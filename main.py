import os

STABILIZATION_LOOP_LIMIT = 100

def initialize_circuit(circuit_file):
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
    file.write("Tempo," + ','.join(signals.keys()) + "\n")

def print_signals(time, signals, file):
    file.write(str(time) + "," + ','.join(map(str, signals.values())) + "\n")

def propagate(circuit, signals):
    signals_temp = signals.copy()
    for entry in circuit:
        if entry[1] == "AND":
            signals_temp[entry[0]] = int(signals[entry[2]] and signals[entry[3]])
        elif entry[1] == "OR":
            signals_temp[entry[0]] = int(signals[entry[2]] or signals[entry[3]])
        elif entry[1] == "NAND":
            signals_temp[entry[0]] = int(not(signals[entry[2]] and signals[entry[3]]))
        elif entry[1] == "NOR":
            signals_temp[entry[0]] = int(not(signals[entry[2]] or signals[entry[3]]))
        elif entry[1] == "XOR":
            signals_temp[entry[0]] = int(signals[entry[2]] ^ signals[entry[3]])
        elif entry[1] == "NOT":
            signals_temp[entry[0]] = int(not(signals[entry[2]]))
        else:
            print("Not valid!")
            exit()
    return signals_temp

def stabilize_0(circuit, signals):
    for _ in range(STABILIZATION_LOOP_LIMIT):
        new_signals = propagate(circuit, signals)
        if signals == new_signals:
            return signals
        else:
            signals = new_signals
    
    print("Circuit did not stabilize!")
    return signals

def stabilize_1(circuit, signals, time, output_file):
    for _ in range(STABILIZATION_LOOP_LIMIT):
        print_signals(time, signals, output_file)
        new_signals = propagate(circuit, signals)
        time += 1
        if signals == new_signals:
            print_signals(time, signals, output_file)
            return
        else:
            signals = new_signals

    print("Circuit did not stabilize!")
    
def main(path):
    circuit_file = open(path + "/circuito.hdl", "r")
    signals_file = open(path + "/estimulos.txt", "r")

    # 0 means no delay and 1 means with delay
    output_0_file = open(path + "/saida0.csv", "w")
    output_1_file = open(path + "/saida1.csv", "w")

    circuit, signals = initialize_circuit(circuit_file)

    signals_0 = signals.copy()
    signals_1 = signals.copy()

    time_0 = 0
    time_1 = 0

    print_header(signals_0, output_0_file)
    print_header(signals_1, output_1_file)

    for line in signals_file:
        if line[0] == "+":
            time_increment = int(line.replace("+", "").replace("\n", ""))

            signals_0 = stabilize_0(circuit, signals_0)

            for _ in range(time_increment):
                print_signals(time_0, signals_0, output_0_file)
                time_0 += 1

            for _ in range(time_increment):
                print_signals(time_1, signals_1, output_1_file)
                signals_1 = propagate(circuit, signals_1)
                time_1 += 1
            
        else:
            (names, values) =  line.split(" = ")
            for (name, value) in zip(names, values):
                signals_0[name] = int(value)
                signals_1[name] = int(value)

    last_signals_0 = signals_0.copy()
    signals_0 = stabilize_0(circuit, signals_0)
    print_signals(time_0, signals_0, output_0_file)

    if last_signals_0 != signals_0:
        print_signals(time_0 + 1, signals_0, output_0_file)

    stabilize_1(circuit, signals_1, time_1, output_1_file)

    output_0_file.close()
    output_1_file.close()

test_folder = "./test"
tests = [name for name in os.listdir(test_folder) if os.path.isdir(os.path.join(test_folder, name))]

for test in tests:
    main("test/" + test)