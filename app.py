from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSpinBox, QDoubleSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
)
import sys
import core.materials as materials
import core.elements

class BeamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BEAM APP")

        self.layout = QHBoxLayout()

        self.column_01 = QVBoxLayout() 
        self.column_02 = QVBoxLayout()
        self.column_03 = QVBoxLayout()

        self.init_materials_input()
        self.init_section_input()
        self.init_rebar_input()
        self.init_stirrups_input()
        self.init_results_section()

        self.layout.addLayout(self.column_01)
        self.layout.addLayout(self.column_02)
        self.layout.addLayout(self.column_03)

        self.setLayout(self.layout)

    def init_materials_input(self):
        self.column_01.addWidget(QLabel("Concrete Compression Strength [MPa]"))
        self.fpc_input = QDoubleSpinBox()
        self.fpc_input.setMinimum(21.0)
        self.fpc_input.setMaximum(10000)
        self.fpc_input.setSingleStep(1.0)
        self.column_01.addWidget(self.fpc_input)

        self.column_01.addWidget(QLabel("Steel Yield Stress [MPa]"))
        self.fy_input = QDoubleSpinBox()
        self.fy_input.setMinimum(420.0)
        self.fy_input.setMaximum(10000)
        self.fy_input.setSingleStep(10.0)
        self.column_01.addWidget(self.fy_input)

    def init_section_input(self):
        self.column_01.addWidget(QLabel("Beam Width [mm]"))
        self.width_input = QSpinBox()
        self.width_input.setMinimum(100.)
        self.width_input.setMaximum(10000)
        self.width_input.setSingleStep(10.0)
        self.column_01.addWidget(self.width_input)

        self.column_01.addWidget(QLabel("Beam Height [mm]"))
        self.height_input = QSpinBox()
        self.height_input.setMinimum(100.)
        self.height_input.setMaximum(10000)
        self.height_input.setSingleStep(10)
        self.column_01.addWidget(self.height_input)

    def init_rebar_input(self):
        self.column_01.addWidget(QLabel("Top Rebar Diameter [mm]"))
        self.top_diam_input = QSpinBox()
        self.top_diam_input.setMinimum(1)
        self.column_01.addWidget(self.top_diam_input)

        self.column_01.addWidget(QLabel("Top Rebar Quantity"))
        self.top_qty_input = QSpinBox()
        self.top_qty_input.setMinimum(1)
        self.column_01.addWidget(self.top_qty_input)

        self.column_01.addWidget(QLabel("Bottom Rebar Diameter [mm]"))
        self.bot_diam_input = QSpinBox()
        self.bot_diam_input.setMinimum(1)
        self.column_01.addWidget(self.bot_diam_input)

        self.column_01.addWidget(QLabel("Bottom Rebar Quantity"))
        self.bot_qty_input = QSpinBox()
        self.bot_qty_input.setMinimum(1)
        self.column_01.addWidget(self.bot_qty_input)

    def init_stirrups_input(self):
        self.column_01.addWidget(QLabel("Stirrup Diameter [mm]"))
        self.stirrup_diam_input = QSpinBox()
        self.stirrup_diam_input.setMinimum(1)
        self.column_01.addWidget(self.stirrup_diam_input)

        self.column_01.addWidget(QLabel("Stirrup Legs"))
        self.stirrup_legs_input = QSpinBox()
        self.stirrup_legs_input.setMinimum(1)
        self.column_01.addWidget(self.stirrup_legs_input)

        self.column_01.addWidget(QLabel("Stirrup Spacing [mm]"))
        self.stirrup_spacing_input = QSpinBox()
        self.stirrup_spacing_input.setMinimum(1)
        self.column_01.addWidget(self.stirrup_spacing_input)

    def init_results_section(self):
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_results)
        self.column_01.addWidget(self.calc_button)

        self.results_table = QTableWidget(17, 4)
        self.results_table.setHorizontalHeaderLabels(["Name", "Variable", "Value", "Units"])
        self.results_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.column_02.addWidget(self.results_table)


    def calculate_results(self):
        Concrete_material = materials.Concrete(
            compression_resistance=self.fpc_input.value()
        )

        Steel_material = materials.Steel(
            yield_stress=self.fy_input.value()
        )

        ConcreteSection = elements.ConcreteSection(
            width=self.width_input.value(),
            height=self.height_input.value(),
            Concrete=Concrete_material
        )

        TopRebar = elements.Rebar(
            diameter=self.top_diam_input.value(),
            quantity=self.top_qty_input.value(),
            Steel=Steel_material
        )

        BottomRebar = elements.Rebar(
            diameter=self.bot_diam_input.value(),
            quantity=self.bot_qty_input.value(),
            Steel=Steel_material
        )

        Stirrup = elements.Stirrup(
            diameter=self.stirrup_diam_input.value(),
            quantity=self.stirrup_legs_input.value(),
            spacing=self.stirrup_spacing_input.value(),
            Steel=Steel_material
        )

        RCB = elements.ReinforcedConcreteBeamSection(
            ConcreteSection=ConcreteSection,
            TopRebar=TopRebar,
            BottomRebar=BottomRebar,
            Stirrup=Stirrup
        )

        values = [
            ("Positive Nominal Moment", "Mn [+]", f"{RCB.get_positive_nominal_moment():.2f}", "N-mm"),
            ("Negative Nominal Moment", "Mn [-]", f"{RCB.get_negative_nominal_moment():.2f}", "N-mm"),
            ("Flexural Reduction Factor", "φ", f"0.90"," "),
            ("Reduced Positive Moment", "φMn [+]", f"{0.9 * RCB.get_positive_nominal_moment():.2f}", "N-mm"),
            ("Reduced Negative Moment", "φMn [-]", f"{0.9 * RCB.get_negative_nominal_moment():.2f}", "N-mm"),
            ("Ultimate Shear Limit for Positive Moment", "Vu [+]", f"{RCB.get_ultimate_shear_limit_for_positive_moment():.2f}", "N"),
            ("Ultimate Shear Limit for Negative Moment", "Vu [-]", f"{RCB.get_ultimate_shear_limit_for_negative_moment():.2f}", "N"),
            ("Nominal Shear Concrete Resistance for positive moment", "Vc [+]", f"{RCB.get_nominal_concrete_shear_strength_for_positive_moment():.2f}", "N"),
            ("Nominal Shear Stirrups Resistance for positive moment", "Vs [+]", f"{RCB.get_nominal_stirrups_shear_strength_for_positive_moment():.2f}", "N"),
            ("Nominal Shear Resistance for positive moment", "Vn [+]", f"{RCB.get_nominal_shear_strength_for_positive_moment():.2f}", "N"),
            ("Shear Reduction Factor", "φ", f"0.60"," "),
            ("Reduced Nominal Shear Resistance for positive moment", "Vn [+]", f"{0.60 *RCB.get_nominal_shear_strength_for_positive_moment():.2f}", "N"),
            ("Nominal Shear Concrete Resistance for negative moment", "Vc [-]", f"{RCB.get_nominal_concrete_shear_strength_for_negative_moment():.2f}", "N"),
            ("Nominal Shear Stirrups Resistance for negative moment", "Vs [-]", f"{RCB.get_nominal_stirrups_shear_strength_for_negative_moment():.2f}", "N"),
            ("Nominal Shear Resistance for negative moment", "Vn [-]", f"{RCB.get_nominal_shear_strength_for_negative_moment():.2f}", "N"),
            ("Shear Reduction Factor", "φ", f"0.60"," "),
            ("Reduced Nominal Shear Resistance for negative moment", "Vn [-]", f"{0.60 *RCB.get_nominal_shear_strength_for_negative_moment():.2f}", "N"),


        ]

        for i, (name, var, val, un) in enumerate(values):
            self.results_table.setItem(i, 0, QTableWidgetItem(name))
            self.results_table.setItem(i, 1, QTableWidgetItem(var))
            self.results_table.setItem(i, 2, QTableWidgetItem(val))
            self.results_table.setItem(i, 3, QTableWidgetItem(un))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BeamApp()
    window.show()
    sys.exit(app.exec())