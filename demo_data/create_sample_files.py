"""
Script to create sample Excel files for demo.
Run this after installing requirements: pip install -r requirements.txt
"""

import pandas as pd
from pathlib import Path

def create_experimental_results():
    """Create experimental results Excel file."""

    data = {
        'Experiment_ID': ['EXP-001', 'EXP-002', 'EXP-003', 'EXP-004', 'EXP-005',
                          'EXP-006', 'EXP-007', 'EXP-008', 'EXP-009', 'EXP-010'],
        'Date': ['2024-01-15', '2024-01-18', '2024-01-22', '2024-01-25', '2024-02-01',
                 '2024-02-05', '2024-02-10', '2024-02-15', '2024-02-20', '2024-02-25'],
        'Researcher': ['Dr. Chen', 'Dr. Martinez', 'Dr. Chen', 'Dr. Wong', 'Dr. Martinez',
                       'Dr. Chen', 'Dr. Wong', 'Dr. Chen', 'Dr. Martinez', 'Dr. Wong'],
        'Method': ['Electrolysis', 'Gas Loading', 'Electrolysis', 'Electrolysis', 'Gas Loading',
                   'Plasma', 'Electrolysis', 'Gas Loading', 'Plasma', 'Electrolysis'],
        'Cathode_Material': ['Palladium', 'Nickel', 'Palladium', 'Palladium', 'Nickel',
                             'Palladium', 'Palladium', 'Nickel', 'Palladium', 'Palladium'],
        'Temperature_C': [25, 300, 30, 28, 350, 80, 35, 320, 75, 32],
        'Pressure_Bar': [1.0, 50.0, 1.0, 1.0, 75.0, 1.2, 1.0, 60.0, 1.5, 1.0],
        'Duration_Hours': [72, 48, 96, 120, 36, 24, 144, 60, 18, 168],
        'Input_Power_W': [50.0, 200.0, 45.0, 55.0, 180.0, 300.0, 48.0, 210.0, 320.0, 52.0],
        'Output_Power_W': [52.0, 235.0, 62.0, 58.0, 205.0, 450.0, 75.0, 238.0, 480.0, 78.0],
        'Excess_Heat_W': [2.0, 35.0, 17.0, 3.0, 25.0, 150.0, 27.0, 28.0, 160.0, 26.0],
        'Excess_Percentage': [4.0, 17.5, 37.8, 5.5, 13.9, 50.0, 56.3, 13.3, 50.0, 50.0],
        'Tritium_Detected': ['No', 'No', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes'],
        'Surface_Changes': ['Minor', 'Moderate', 'Significant', 'Minor', 'Moderate',
                            'Significant', 'Significant', 'Moderate', 'Significant', 'Significant'],
        'Success': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']
    }

    df = pd.DataFrame(data)

    with pd.ExcelWriter('demo_data/experimental_results.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Experiments', index=False)

        # Summary sheet
        summary = pd.DataFrame({
            'Metric': ['Total Experiments', 'Success Rate', 'Average Excess Heat (W)',
                       'Max Excess Heat (W)', 'Tritium Detection Rate', 'Most Common Method',
                       'Average Duration (hours)'],
            'Value': [
                len(df),
                '100%',
                f"{df['Excess_Heat_W'].mean():.1f}",
                f"{df['Excess_Heat_W'].max():.1f}",
                f"{(df['Tritium_Detected'] == 'Yes').sum() / len(df) * 100:.0f}%",
                df['Method'].mode()[0],
                f"{df['Duration_Hours'].mean():.1f}"
            ]
        })
        summary.to_excel(writer, sheet_name='Summary', index=False)

    print('✓ Created: experimental_results.xlsx')


def create_temperature_pressure_data():
    """Create temperature and pressure monitoring data."""

    import numpy as np

    # Time series data
    time_points = list(range(0, 121, 5))  # 0 to 120 minutes, every 5 minutes

    data = {
        'Time_Minutes': time_points,
        'Temperature_C': [25 + i*0.5 + np.random.normal(0, 0.5) for i in range(len(time_points))],
        'Pressure_Bar': [1.0 + i*0.01 + np.random.normal(0, 0.02) for i in range(len(time_points))],
        'Input_Power_W': [50.0 + np.random.normal(0, 1.0) for _ in time_points],
        'Output_Power_W': [52.0 + i*0.2 + np.random.normal(0, 1.5) for i in range(len(time_points))],
        'Excess_Power_W': [2.0 + i*0.2 + np.random.normal(0, 1.0) for i in range(len(time_points))],
    }

    df = pd.DataFrame(data)

    with pd.ExcelWriter('demo_data/temperature_pressure_data.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='TimeSeries', index=False)

        # Statistics sheet
        stats = pd.DataFrame({
            'Parameter': ['Temperature (C)', 'Pressure (Bar)', 'Input Power (W)',
                          'Output Power (W)', 'Excess Power (W)'],
            'Mean': [df['Temperature_C'].mean(), df['Pressure_Bar'].mean(),
                     df['Input_Power_W'].mean(), df['Output_Power_W'].mean(),
                     df['Excess_Power_W'].mean()],
            'Min': [df['Temperature_C'].min(), df['Pressure_Bar'].min(),
                    df['Input_Power_W'].min(), df['Output_Power_W'].min(),
                    df['Excess_Power_W'].min()],
            'Max': [df['Temperature_C'].max(), df['Pressure_Bar'].max(),
                    df['Input_Power_W'].max(), df['Output_Power_W'].max(),
                    df['Excess_Power_W'].max()],
        })
        stats.to_excel(writer, sheet_name='Statistics', index=False)

    print('✓ Created: temperature_pressure_data.xlsx')


def create_materials_database():
    """Create materials properties database."""

    data = {
        'Material': ['Palladium', 'Nickel', 'Platinum', 'Titanium', 'Zirconium',
                     'Lithium', 'Deuterium', 'Heavy Water'],
        'Symbol': ['Pd', 'Ni', 'Pt', 'Ti', 'Zr', 'Li', 'D', 'D2O'],
        'Atomic_Number': [46, 28, 78, 22, 40, 3, 1, '-'],
        'Category': ['Metal', 'Metal', 'Metal', 'Metal', 'Metal', 'Metal', 'Isotope', 'Compound'],
        'Melting_Point_C': [1554.9, 1455, 1768.3, 1668, 1855, 180.5, -254.4, 3.82],
        'Density_g_cm3': [12.02, 8.91, 21.45, 4.51, 6.52, 0.534, 0.18, 1.11],
        'Crystal_Structure': ['FCC', 'FCC', 'FCC', 'HCP', 'HCP', 'BCC', '-', '-'],
        'H_Solubility': ['High', 'Moderate', 'Moderate', 'High', 'Very High', '-', '-', '-'],
        'Cost_per_kg_USD': [60000, 18, 31000, 35, 150, 185, 2000, 800],
        'LENR_Usage': ['Cathode', 'Cathode', 'Anode', 'Cathode', 'Cathode', 'Electrolyte', 'Fuel', 'Solvent'],
        'Notes': [
            'Most studied material for LENR',
            'Alternative to Pd, lower cost',
            'Used as anode in electrolysis',
            'High H absorption, less studied',
            'Highest H absorption capacity',
            'Common electrolyte component',
            'Fuel isotope',
            'Solvent for electrolysis'
        ]
    }

    df = pd.DataFrame(data)

    with pd.ExcelWriter('demo_data/materials_database.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Materials', index=False)

        # Cathode materials comparison
        cathodes = df[df['LENR_Usage'] == 'Cathode'].copy()
        cathodes_summary = cathodes[['Material', 'H_Solubility', 'Cost_per_kg_USD', 'Notes']]
        cathodes_summary.to_excel(writer, sheet_name='Cathode_Comparison', index=False)

    print('✓ Created: materials_database.xlsx')


def create_publication_timeline():
    """Create research publication timeline."""

    data = {
        'Year': [1989, 1990, 1991, 1995, 2000, 2004, 2008, 2012, 2015, 2019, 2022, 2024],
        'Authors': [
            'Fleischmann & Pons',
            'Various researchers',
            'Storms et al.',
            'McKubre et al.',
            'Arata & Zhang',
            'DOE Review Panel',
            'U.S. Navy Research',
            'Rossi & Focardi',
            'NASA Langley',
            'NASA Technical Report',
            'Multiple Groups',
            'International Consortium'
        ],
        'Title': [
            'Electrochemically induced nuclear fusion of deuterium',
            'Replication attempts worldwide',
            'Review of cold fusion research',
            'Excess power observations in electrochemical studies',
            'DS-Reactor experiments',
            'Review of Low Energy Nuclear Reactions',
            'Thermal and Nuclear Aspects of Pd/D2O System',
            'E-Cat demonstration and testing',
            'Low Energy Nuclear Reactions review',
            'LENR Technology - A Comprehensive Review',
            'Multiple positive replications reported',
            'Standardized protocols and reproducibility'
        ],
        'Institution': [
            'University of Utah',
            'Various',
            'Los Alamos National Laboratory',
            'SRI International',
            'Osaka University',
            'U.S. Department of Energy',
            'U.S. Naval Research Laboratory',
            'University of Bologna',
            'NASA Langley Research Center',
            'NASA',
            'Various',
            'ILENR Consortium'
        ],
        'Type': [
            'Original Discovery',
            'Replication Studies',
            'Review',
            'Experimental',
            'Experimental',
            'Government Review',
            'Experimental',
            'Commercial Demo',
            'Review',
            'Technical Report',
            'Experimental',
            'Standardization'
        ],
        'Citations': [2500, 150, 300, 180, 120, 450, 200, 85, 95, 150, 45, 12],
        'Significance': [
            'Field-defining announcement',
            'Mixed replication results',
            'Comprehensive early review',
            'Documented excess heat',
            'Novel reactor design',
            'Acknowledged scientific merit',
            'Military interest',
            'Commercial interest',
            'NASA endorsement',
            'Detailed mechanisms',
            'Improving reproducibility',
            'Standardized methods'
        ]
    }

    df = pd.DataFrame(data)

    with pd.ExcelWriter('demo_data/publication_timeline.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Timeline', index=False)

        # Decade summary
        df['Decade'] = (df['Year'] // 10) * 10
        decade_summary = df.groupby('Decade').agg({
            'Year': 'count',
            'Citations': 'sum'
        }).rename(columns={'Year': 'Publications', 'Citations': 'Total_Citations'})
        decade_summary.to_excel(writer, sheet_name='Decade_Summary')

    print('✓ Created: publication_timeline.xlsx')


def main():
    """Create all sample files."""
    print("\n" + "="*50)
    print("Creating Sample Data Files")
    print("="*50 + "\n")

    try:
        create_experimental_results()
        create_temperature_pressure_data()
        create_materials_database()
        create_publication_timeline()

        print("\n" + "="*50)
        print("✓ All sample files created successfully!")
        print("="*50 + "\n")

        print("Files created in demo_data/:")
        print("  • experimental_results.xlsx")
        print("  • temperature_pressure_data.xlsx")
        print("  • materials_database.xlsx")
        print("  • publication_timeline.xlsx")
        print("\nYou can now upload these files to the RAG system!")

    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease install required packages first:")
        print("  pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Error creating files: {e}")


if __name__ == "__main__":
    main()
