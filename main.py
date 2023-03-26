import os

# Limit of signal propagations for the circuit to stabilize.
STABILIZATION_LOOP_LIMIT = 1000


def initialize_circuit(circuit_file):
    """
    Reads and initialize the circuit from its file. This will also return the signals 
    dictionary with all values set to 0.
    """

    circuit = []
    signals = dict()

    for line in circuit_file:
        tokens = line.split()

        signals[tokens[0]] = 0
        signals[tokens[3]] = 0

        if tokens[2] == 'NOT':
            circuit.append((tokens[0], tokens[2], tokens[3]))
        else:
            signals[tokens[4]] = 0
            circuit.append((tokens[0], tokens[2], tokens[3], tokens[4]))

    return (circuit, dict(sorted(signals.items())))


def print_header(signals, file):
    """
    Prints CSV header for specified signals on output file.
    """

    file.write("Tempo," + ','.join(signals.keys()) + "\n")


def print_signals(time, signals, file):
    """
    Print signals values for a certain time on the output file.
    """

    file.write(str(time) + "," + ','.join(map(str, signals.values())) + "\n")


def propagate(circuit, signals):
    """
    Propagates all signals in a circuit one time, and returns the new signals state.
    """

    signals_temp = signals.copy()
    for entry in circuit:
        if entry[1] == "AND":
            signals_temp[entry[0]] = int(
                signals[entry[2]] and signals[entry[3]])
        elif entry[1] == "OR":
            signals_temp[entry[0]] = int(
                signals[entry[2]] or signals[entry[3]])
        elif entry[1] == "NAND":
            signals_temp[entry[0]] = int(
                not (signals[entry[2]] and signals[entry[3]]))
        elif entry[1] == "NOR":
            signals_temp[entry[0]] = int(
                not (signals[entry[2]] or signals[entry[3]]))
        elif entry[1] == "XOR":
            signals_temp[entry[0]] = int(signals[entry[2]] ^ signals[entry[3]])
        elif entry[1] == "NOT":
            signals_temp[entry[0]] = int(not (signals[entry[2]]))
        else:
            print("Not valid!")
            exit()
    return signals_temp


def stabilize(circuit, signals, time=0, output_file=None):
    """
    Propagates all signals in the circuit until it stabilizes, returning back the final signals.
    If the circuit doesn't stabilize in a certain number of iterations, the function will not attempt
    to stabilize it anymore and will return the latest state of the signals.

    If an output file is specified along with an initial time, all intermediate states until the
    circuit stabilizes will be outputed to the file.
    """

    for _ in range(STABILIZATION_LOOP_LIMIT):
        if output_file:
            print_signals(time, signals, output_file)

        new_signals = propagate(circuit, signals)
        time += 1
        if signals == new_signals:
            if output_file:
                print_signals(time, signals, output_file)
            return signals
        else:
            signals = new_signals

    print("Circuit did not stabilize in " +
          str(STABILIZATION_LOOP_LIMIT) + " iterations!")
    return signals


def simulate_circuit(path):
    """
    Simulates the circuit defined in the specified path, on the files "circuito.hdl" and "estimulos.txt".

    The output of simulation disregarding propagation delay will be written to the file "saida0.txt", and
    the simulation considering the signal delay will be written to "saida1.txt".
    """

    circuit_file = open(path + "/circuito.hdl", "r")
    signals_file = open(path + "/estimulos.txt", "r")

    # 0 = ignoring propagation delay, 1 = considering propagation delay
    output_0_file = open(path + "/saida0.csv", "w")
    output_1_file = open(path + "/saida1.csv", "w")

    circuit, signals = initialize_circuit(circuit_file)

    signals_0 = signals.copy()
    signals_1 = signals.copy()

    time = 0

    print_header(signals_0, output_0_file)
    print_header(signals_1, output_1_file)

    for line in signals_file:
        if line[0] == "+":
            time_increment = int(line)

            signals_0 = stabilize(circuit, signals_0)

            for _ in range(time_increment):
                print_signals(time, signals_0, output_0_file)
                print_signals(time, signals_1, output_1_file)
                signals_1 = propagate(circuit, signals_1)
                time += 1
        else:
            (names, values) = line.split(" = ")
            for (name, value) in zip(names, values):
                signals_0[name] = int(value)
                signals_1[name] = int(value)

    signals_0 = stabilize(circuit, signals_0)
    print_signals(time, signals_0, output_0_file)
    print_signals(time + 1, signals_0, output_0_file)

    stabilize(circuit, signals_1, time, output_1_file)

    output_0_file.close()
    output_1_file.close()

def main():
    test_folder = "./test"
    tests = [name for name in os.listdir(
        test_folder) if os.path.isdir(os.path.join(test_folder, name))]

    for test in tests:
        simulate_circuit("test/" + test)

if __name__ == "__main__":
    main()
