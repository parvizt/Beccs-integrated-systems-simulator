# Name: BECCS Integrated Systems Simulator Pro
# Version: 1.4
# Date: 2026-09-02 (Miladi)
# Header: AiBrothersTools.ir

import sys
import os
import sqlite3
import csv
from dataclasses import dataclass
import numpy as np

try:
    from PyQt5 import QtWidgets, QtCore, QtGui
    from PyQt5.QtPrintSupport import QPrinter
    import pyqtgraph as pg
except ImportError as e:
    print(f"Error: {e}.   PyQt5 and pyqtgraph : Please add libraries:  .")
    sys.exit(1)


@dataclass
class SimulationKPIs:
    gross_captured: float = 0.0
    transported: float = 0.0
    injected: float = 0.0
    net_stored: float = 0.0
    net_ggr_removal: float = 0.0
    cum_leakage: float = 0.0
    mineralized: float = 0.0


class BECCSSimulator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AiBrothersTools.ir - BECCS Systems Simulator Pro v1.4")
        self.setGeometry(100, 100, 1350, 850)
        if os.path.exists('d:/l.ico'):
            self.setWindowIcon(QtGui.QIcon('d:/l.ico'))
        
        self.db_name = "beccs_records.db"
        self.is_authenticated = False
        
        # Base font size
        self.base_font_size = 7
        
        # Crosshair storage data
        self.curr_x = np.array([])
        self.curr_gross = np.array([])
        self.curr_inj = np.array([])
        self.curr_net = np.array([])
        self.curr_leak = np.array([])
        self.curr_min = np.array([])
        self.unit_factor = 1000.0  # Default kTons
        self.unit_name = "kTons"
        
        self.init_db()
        self.init_ui()
        self.apply_styles()
        self.log_msg("System Initialized. Awaiting Authentication.")

    def init_db(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sim_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        env_type TEXT,
                        biomass REAL,
                        cap_eff REAL,
                        cap_limit REAL,
                        duration INTEGER,
                        net_stored REAL,
                        net_ggr REAL
                    )
                """)
                conn.commit()
        except Exception as e:
            self.show_error("  Error in create database ", e)

    def apply_styles(self):
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: #1e1e1e; color: #d4d4d4; }}
            QWidget {{ font-size: {self.base_font_size}pt; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            QGroupBox {{ 
                color: #00BFFF; 
                font-weight: bold; 
                border: 1px solid #555; 
                margin-top: 15px; 
                font-size: {self.base_font_size + 1}pt; 
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 3px; }}
            QLineEdit {{ 
                background-color: #333; 
                color: green; 
                border: 1px solid #555; 
                padding: 4px; 
                border-radius: 3px;
            }}
            QComboBox {{ 
                background-color: #333; 
                color: #FFFFFF; 
                border: 1px solid #555; 
                padding: 4px; 
                border-radius: 3px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #2b2b2b;
                color: #FFFFFF;
                selection-background-color: #0078D7;
                selection-color: #FFFFFF;
                border: 1px solid #555;
                outline: none;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QTableWidget {{ background-color: #2b2b2b; color: white; gridline-color: #555; }}
            QHeaderView::section {{ background-color: #333; color: white; padding: 4px; border: 1px solid #555; }}
            QTabWidget::pane {{ border: 1px solid #444; }}
            QTabBar::tab {{ background: #333; color: #aaa; padding: 6px 12px; border: 1px solid #444; }}
            QTabBar::tab:selected {{ background: #555; color: white; font-weight: bold; }}
            QPushButton {{ color: white; border-radius: 4px; padding: 5px; font-weight: bold; }}
            QPushButton#btnAuth {{ background-color: #00BFFF; color: #000; }}
            QPushButton#btnRun {{ background-color: #0078D7; }}
            QPushButton#btnPdf {{ background-color: #8A2BE2; }}
            QPushButton#btnExcel {{ background-color: #008080; }}
            QPushButton#btnExit {{ background-color: #E81123; }}
            QPushButton#btnClearDB {{ background-color: #D2691E; }}
            QPushButton:hover {{ opacity: 0.8; border: 1px solid white; }}
        """)

    def init_ui(self):
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.scroll_area)

        self.main_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.main_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)

        self.setup_header()
        self.setup_tabs()
        self.setup_logger()

    def setup_header(self):
        header_layout = QtWidgets.QHBoxLayout()
        
        title = QtWidgets.QLabel("BECCS Integrated Systems Simulator v1.4")
        title.setStyleSheet(f"color: white; font-size: {self.base_font_size + 6}pt; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()

        self.pw_input = QtWidgets.QLineEdit()
        self.pw_input.setPlaceholderText("Auth PW (admin)")
        self.pw_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pw_input.setFixedWidth(120)
        header_layout.addWidget(self.pw_input)

        self.btn_auth = QtWidgets.QPushButton("Unlock")
        self.btn_auth.setObjectName("btnAuth")
        self.btn_auth.clicked.connect(self.authenticate)
        header_layout.addWidget(self.btn_auth)

        watermark = QtWidgets.QLabel("AiBrothersTools.ir")
        watermark.setStyleSheet("color: #888; font-style: italic; margin-left: 10px;")
        header_layout.addWidget(watermark)

        self.main_layout.addLayout(header_layout)

        self.desc_label = QtWidgets.QLabel(
            "“This simulation framework mimics the lifecycle of carbon sequestration by integrating "
            "biomass input variables with subsurface storage constraints, demonstrating a systems-thinking "
            "approach to geological engineering.”"
        )
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet(f"color: #FF3333; font-style: italic; font-size: {self.base_font_size + 1}pt; padding: 5px 0;")
        self.main_layout.addWidget(self.desc_label)

    def setup_tabs(self):
        self.tabs = QtWidgets.QTabWidget()
        self.tab_sim = QtWidgets.QWidget()
        self.tab_db = QtWidgets.QWidget()
        
        self.tabs.addTab(self.tab_sim, "Algorithm (Simulation)")
        self.tabs.addTab(self.tab_db, "Records (DB)")
        
        self.main_layout.addWidget(self.tabs)
        
        self.setup_sim_tab()
        self.setup_db_tab()

    def setup_sim_tab(self):
        layout = QtWidgets.QHBoxLayout(self.tab_sim)
        
        # Left Panel
        left_panel = QtWidgets.QVBoxLayout()
        left_panel.setAlignment(QtCore.Qt.AlignTop)
        
        group_inputs = QtWidgets.QGroupBox("Geological_Biomass Parameters")
        form_layout = QtWidgets.QFormLayout(group_inputs)
        
        blue_label_style = "color: #00BFFF; font-weight: bold;"

        lbl_env = QtWidgets.QLabel("Geological Env:")
        lbl_env.setStyleSheet(blue_label_style)
        self.cmb_env = QtWidgets.QComboBox()
        self.cmb_env.addItems(["Saline Aquifer", "Depleted Oil/Gas", "Basalt"])
        form_layout.addRow(lbl_env, self.cmb_env)
        
        # Display Unit Selector (Tons, kTons, MTons)
        lbl_unit = QtWidgets.QLabel("Display Unit:")
        lbl_unit.setStyleSheet(blue_label_style)
        self.cmb_unit = QtWidgets.QComboBox()
        self.cmb_unit.addItems(["kTons (10³ Tons)", "MTons (10⁶ Tons)", "Tons"])
        self.cmb_unit.currentIndexChanged.connect(self.on_unit_change)
        form_layout.addRow(lbl_unit, self.cmb_unit)
        
        lbl_bio = QtWidgets.QLabel("Annual Biomass (Tons):")
        lbl_bio.setStyleSheet(blue_label_style)
        self.txt_biomass = QtWidgets.QLineEdit("1500")
        form_layout.addRow(lbl_bio, self.txt_biomass)
        
        lbl_eff = QtWidgets.QLabel("Capture Efficiency (0-1):")
        lbl_eff.setStyleSheet(blue_label_style)
        self.txt_efficiency = QtWidgets.QLineEdit("0.92")
        form_layout.addRow(lbl_eff, self.txt_efficiency)
        
        lbl_cap = QtWidgets.QLabel("Capacity Limit (Tons):")
        lbl_cap.setStyleSheet(blue_label_style)
        self.txt_capacity = QtWidgets.QLineEdit("50000")
        form_layout.addRow(lbl_cap, self.txt_capacity)
        
        lbl_dur = QtWidgets.QLabel("Sim Duration (Years):")
        lbl_dur.setStyleSheet(blue_label_style)
        self.txt_duration = QtWidgets.QLineEdit("30")
        form_layout.addRow(lbl_dur, self.txt_duration)
        
        left_panel.addWidget(group_inputs)

        # KPI Panel
        self.group_kpi = QtWidgets.QGroupBox("KPI Metrics (kTons)")
        self.group_kpi.setStyleSheet("QGroupBox { color: #008040; }")
        self.kpi_layout = QtWidgets.QFormLayout(self.group_kpi)
        self.kpi_labels = {}
        
        metrics = [
            ("Gross Captured", "gross_captured"),
            ("Transported", "transported"),
            ("Injected", "injected"),
            ("Net Stored", "net_stored"),
            ("Net GGR Removal", "net_ggr_removal"),
            ("Cum. Leakage", "cum_leakage"),
            ("Mineralized", "mineralized")
        ]
        
        dark_green_style = "color: #008040; font-weight: bold;"
        for label_text, attr_name in metrics:
            lbl = QtWidgets.QLabel(f"{label_text}:")
            lbl.setStyleSheet(dark_green_style)
            val = QtWidgets.QLabel("0.00")
            val.setStyleSheet(dark_green_style)
            self.kpi_layout.addRow(lbl, val)
            self.kpi_labels[attr_name] = val
            
        left_panel.addWidget(self.group_kpi)
        
        # Buttons Panel
        btn_layout = QtWidgets.QGridLayout()
        
        self.btn_run = QtWidgets.QPushButton("Simulate")
        self.btn_run.setObjectName("btnRun")
        self.btn_run.clicked.connect(self.run_simulation)
        
        self.btn_pdf = QtWidgets.QPushButton("Export PDF")
        self.btn_pdf.setObjectName("btnPdf")
        self.btn_pdf.clicked.connect(self.export_pdf)

        self.btn_excel = QtWidgets.QPushButton("Export Excel")
        self.btn_excel.setObjectName("btnExcel")
        self.btn_excel.clicked.connect(self.export_excel)
        
        self.btn_exit = QtWidgets.QPushButton("Exit")
        self.btn_exit.setObjectName("btnExit")
        self.btn_exit.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_run, 0, 0, 1, 2)
        btn_layout.addWidget(self.btn_pdf, 1, 0)
        btn_layout.addWidget(self.btn_excel, 1, 1)
        btn_layout.addWidget(self.btn_exit, 2, 0, 1, 2)
        
        left_panel.addLayout(btn_layout)
        
        self.sim_container = QtWidgets.QWidget()
        self.sim_container.setLayout(left_panel)
        self.sim_container.setEnabled(False)
        
        self.setup_graph()
        
        layout.addWidget(self.sim_container, stretch=1)
        layout.addWidget(self.graph_widget, stretch=3)

    def setup_graph(self):
        pg.setConfigOption('background', '#2b2b2b')
        pg.setConfigOption('foreground', 'w')
        self.graph_widget = pg.PlotWidget(title="Mass Balance Chain: Carbon Trajectory ⚙️")
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)
        self.graph_widget.setLabel('left', 'Cumulative Mass', units='kTons')
        self.graph_widget.setLabel('bottom', 'Time', units='Years')
        self.graph_widget.addLegend(offset=(-10, 10))

        # Crosshair Lines
        self.v_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#FFFF00', width=1, style=QtCore.Qt.DashLine))
        self.h_line = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#FFFF00', width=1, style=QtCore.Qt.DashLine))
        self.graph_widget.addItem(self.v_line, ignoreBounds=True)
        self.graph_widget.addItem(self.h_line, ignoreBounds=True)

        # Crosshair Tooltip
        self.cursor_text = pg.TextItem(anchor=(0, 1), color='#FFFF00')
        self.cursor_text.setFont(QtGui.QFont("Segoe UI", self.base_font_size + 1, QtGui.QFont.Bold))
        self.graph_widget.addItem(self.cursor_text, ignoreBounds=True)

        self.proxy = pg.SignalProxy(self.graph_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

    def on_unit_change(self):
        unit_text = self.cmb_unit.currentText()
        if "kTons" in unit_text:
            self.unit_factor = 1000.0
            self.unit_name = "kTons"
        elif "MTons" in unit_text:
            self.unit_factor = 1000000.0
            self.unit_name = "MTons"
        else:
            self.unit_factor = 1.0
            self.unit_name = "Tons"
            
        self.group_kpi.setTitle(f"KPI Metrics ({self.unit_name})")
        self.graph_widget.setLabel('left', 'Cumulative Mass', units=self.unit_name)
        if len(self.curr_x) > 0:
            self.run_simulation()

    def mouse_moved(self, evt):
        pos = evt[0]
        if self.graph_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.graph_widget.plotItem.vb.mapSceneToView(pos)
            x_val = mouse_point.x()
            y_val = mouse_point.y()
            
            self.v_line.setPos(x_val)
            self.h_line.setPos(y_val)
            
            if len(self.curr_x) > 0:
                idx = int(np.clip(round(x_val), 0, len(self.curr_x) - 1))
                t_val = self.curr_x[idx]
                g_val = self.curr_gross[idx] / self.unit_factor
                i_val = self.curr_inj[idx] / self.unit_factor
                n_val = self.curr_net[idx] / self.unit_factor
                m_val = self.curr_min[idx] / self.unit_factor
                l_val = self.curr_leak[idx] / self.unit_factor
                
                info = (f"Yr: {t_val:.0f} | Y: {y_val:.2f} {self.unit_name}\n"
                        f"Gross Cap: {g_val:.2f}\n"
                        f"Injected: {i_val:.2f}\n"
                        f"Net Stored: {n_val:.2f}\n"
                        f"Mineralized: {m_val:.2f}\n"
                        f"Cum Leak: {l_val:.2f}")
                self.cursor_text.setText(info)
            else:
                self.cursor_text.setText(f"Yr: {x_val:.1f}, Mass: {y_val:.2f} {self.unit_name}")
                
            self.cursor_text.setPos(x_val, y_val)

    def setup_db_tab(self):
        layout = QtWidgets.QVBoxLayout(self.tab_db)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Env", "Biomass", "Eff", "Limit", "Duration", "Net Stored", "Net GGR"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table)

        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_load_db = QtWidgets.QPushButton("Load Records 📊")
        self.btn_load_db.clicked.connect(self.load_records)
        
        self.btn_clear_db = QtWidgets.QPushButton("Clear DB 🗑️")
        self.btn_clear_db.setObjectName("btnClearDB")
        self.btn_clear_db.clicked.connect(self.clear_db)
        
        btn_layout.addWidget(self.btn_load_db)
        btn_layout.addWidget(self.btn_clear_db)
        layout.addLayout(btn_layout)

    def setup_logger(self):
        self.logger = QtWidgets.QTextEdit()
        self.logger.setReadOnly(True)
        self.logger.setFixedHeight(120)
        self.logger.setStyleSheet("background-color: #121212; color: #00FF00; font-family: Consolas;")
        self.main_layout.addWidget(self.logger)

    def log_msg(self, msg):
        dt = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.logger.append(f"[{dt}] 🔬 {msg}")

    def show_error(self, title, exc):
        self.log_msg(f"ERROR: {title} - {str(exc)}")
        print(f"Exception -> {title}: {exc}\nAI Translating to FA: خطایی در اجرای سیستم رخ داد. لطفا لاگ را بررسی کنید.")

    def authenticate(self):
        if self.pw_input.text() == "admin":
            self.is_authenticated = True
            self.sim_container.setEnabled(True)
            self.pw_input.setDisabled(True)
            self.btn_auth.setDisabled(True)
            self.btn_auth.setText("Unlocked ✅")
            self.btn_auth.setStyleSheet("background-color: #32CD32; color: black;")
            self.log_msg("Authentication successful. System is now ready for computation.")
        else:
            self.log_msg("Auth Failed. Access Denied.")
            QtWidgets.QMessageBox.warning(self, "Auth Error", " The password is not correct.\n(Invalid Password)")

    def run_simulation(self):
        try:
            env = self.cmb_env.currentText()
            bio = float(self.txt_biomass.text())
            eff = float(self.txt_efficiency.text())
            cap = float(self.txt_capacity.text())
            dur = int(self.txt_duration.text())
            
            # --- Geological & BECCS Lifecycle Mathematics ---
            years = np.arange(dur + 1)
            gross_cap = bio * eff * years
            transport_loss = 0.015 * gross_cap
            transported = gross_cap - transport_loss
            injected = np.minimum(transported, cap)
            
            # Subsurface Environment Rates
            if env == "Basalt":
                # CarbFix: Fast in-situ mineralization (up to 85%), near-zero leakage
                leak_rate = 0.0001
                cum_leakage = injected * (1.0 - np.exp(-leak_rate * years))
                mineralized = (injected - cum_leakage) * (1.0 - np.exp(-0.45 * years))
            elif env == "Depleted Oil/Gas":
                # Depleted reservoir: Structural trapping dominates, moderate mineralization (5%)
                leak_rate = 0.0015
                cum_leakage = injected * (1.0 - np.exp(-leak_rate * years))
                mineralized = (injected - cum_leakage) * 0.05 * (1.0 - np.exp(-0.05 * years))
            else:  # Saline Aquifer
                # Saline aquifer: Solubility & hydrodynamic trapping, slow mineralization (2%)
                leak_rate = 0.004
                cum_leakage = injected * (1.0 - np.exp(-leak_rate * years))
                mineralized = (injected - cum_leakage) * 0.02 * (1.0 - np.exp(-0.02 * years))
            
            net_stored = injected - cum_leakage
            net_ggr = net_stored - transport_loss
            
            # Store full values
            self.curr_x = years
            self.curr_gross = gross_cap
            self.curr_inj = injected
            self.curr_net = net_stored
            self.curr_leak = cum_leakage
            self.curr_min = mineralized
            
            # Updating KPIs in the selected Unit
            factor = self.unit_factor
            self.kpi_labels['gross_captured'].setText(f"{gross_cap[-1]/factor:.2f}")
            self.kpi_labels['transported'].setText(f"{transported[-1]/factor:.2f}")
            self.kpi_labels['injected'].setText(f"{injected[-1]/factor:.2f}")
            self.kpi_labels['net_stored'].setText(f"{net_stored[-1]/factor:.2f}")
            self.kpi_labels['net_ggr_removal'].setText(f"{net_ggr[-1]/factor:.2f}")
            self.kpi_labels['cum_leakage'].setText(f"{cum_leakage[-1]/factor:.2f}")
            self.kpi_labels['mineralized'].setText(f"{mineralized[-1]/factor:.2f}")
            
            self.plot_results(years, gross_cap/factor, injected/factor, net_stored/factor, cum_leakage/factor, mineralized/factor)
            self.save_record(env, bio, eff, cap, dur, net_stored[-1]/factor, net_ggr[-1]/factor)
            self.log_msg(f"Simulation completed for {env}. GGR: {net_ggr[-1]/factor:.2f} {self.unit_name}")
            
        except ValueError as ve:
            self.show_error("Value Error", ve)
            QtWidgets.QMessageBox.critical(self, "Input Error", "مقادیر وارد شده نامعتبر است.\nCheck input formats.")
        except Exception as e:
            self.show_error("Execution Error", e)

    def plot_results(self, x, gross, inj, net, leak, mineralized):
        self.graph_widget.clear()
        
        # Re-attach Crosshair Elements
        self.graph_widget.addItem(self.v_line, ignoreBounds=True)
        self.graph_widget.addItem(self.h_line, ignoreBounds=True)
        self.graph_widget.addItem(self.cursor_text, ignoreBounds=True)
        
        # 5 Distinct Lines & Colors
        self.graph_widget.plot(x, gross, pen=pg.mkPen(color='#00FFFF', width=2), name="1. Gross Captured (Cyan)")
        self.graph_widget.plot(x, inj, pen=pg.mkPen(color='#FFA500', width=2), name="2. Injected (Orange)")
        self.graph_widget.plot(x, net, pen=pg.mkPen(color='#00FF00', width=2.5), name="3. Net Stored (Green)")
        self.graph_widget.plot(x, mineralized, pen=pg.mkPen(color='#FF00FF', width=2.5, style=QtCore.Qt.DashLine), name="4. Mineralized (Magenta)")
        self.graph_widget.plot(x, leak, pen=pg.mkPen(color='#FF3333', width=2, style=QtCore.Qt.DotLine), name="5. Cum Leakage (Red)")

    def save_record(self, env, bio, eff, cap, dur, net_s, net_g):
        try:
            dt = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm")
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO sim_records (timestamp, env_type, biomass, cap_eff, cap_limit, duration, net_stored, net_ggr) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (dt, env, bio, eff, cap, dur, net_s, net_g)
                )
                conn.commit()
            self.log_msg("Data stored to SQLite3 db successfully.")
        except Exception as e:
            self.show_error("DB Save Error", e)

    def load_records(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sim_records ORDER BY id DESC")
                rows = cursor.fetchall()
                
            self.table.setRowCount(0)
            for row_idx, row_data in enumerate(rows):
                self.table.insertRow(row_idx)
                for col_idx, col_data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_data))
                    if col_idx >= 7 and col_data is not None:
                        item = QtWidgets.QTableWidgetItem(f"{float(col_data):.2f}")
                    self.table.setItem(row_idx, col_idx, item)
            self.log_msg(f"Loaded {len(rows)} records from Database.")
        except Exception as e:
            self.show_error("DB Load Error", e)

    def clear_db(self):
        reply = QtWidgets.QMessageBox.question(
            self, 'Clear DB', 'Are you sure you want to delete all records?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM sim_records")
                    conn.commit()
                self.table.setRowCount(0)
                self.log_msg("Database records cleared.")
            except Exception as e:
                self.show_error("DB Clear Error", e)

    def export_pdf(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName("BECCS_Report_Export.pdf")
            
            painter = QtGui.QPainter()
            if painter.begin(printer):
                screen_pixmap = self.tab_sim.grab()
                rect = painter.viewport()
                size = screen_pixmap.size()
                size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(screen_pixmap.rect())
                painter.drawPixmap(0, 0, screen_pixmap)
                painter.end()
                self.log_msg("Report exported to BECCS_Report_Export.pdf successfully.")
                QtWidgets.QMessageBox.information(self, "Export", "PDF Report saved successfully.")
        except Exception as e:
            self.show_error("PDF Export Error", e)

    def export_excel(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sim_records")
                rows = cursor.fetchall()
            
            with open("BECCS_DB_Export.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Timestamp", "Env Type", "Biomass", "Cap Eff", "Cap Limit", "Duration", "Net Stored", "Net GGR"])
                writer.writerows(rows)
                
            self.log_msg("Data exported to BECCS_DB_Export.csv successfully (Excel compatible).")
            QtWidgets.QMessageBox.information(self, "Export", "CSV Export saved successfully.")
        except Exception as e:
            self.show_error("Excel Export Error", e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    main_win = BECCSSimulator()
    main_win.show()
    sys.exit(app.exec_())
