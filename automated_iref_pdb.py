import subprocess

serial_numbers = ['20UPGM24220370', '20UPGM24220372', '20UPGM24220401', '20UPGM24220402', '20UPGM24220404']

for sn in serial_numbers:
    print(f"Running for serial number: {sn}")
    result = subprocess.run(
        ['python', 'set_iref_trim_pdb.py', '--execute', sn],
        capture_output=True, text=True
    )

    print("Output:", result.stdout)
    print("Errors:", result.stderr)
    print('-' * 40)
