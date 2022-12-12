from day_10_part_one import read_data_file, process_cathode_signal_data, Instruction, process_instructions, fetch_cycles



def test_process_sample_input_2():
    instructions = process_cathode_signal_data(read_data_file('test_2_input.txt'))
    signal_strengths = process_instructions(instructions)
    cycles_under_interest = [20, 60, 100, 140, 180, 220]
    processed_data = fetch_cycles(signal_strengths, cycles_under_interest)
    actual_signal_strengths = [cycle * value for cycle, value in zip(cycles_under_interest, processed_data)]
    assert actual_signal_strengths == [420, 1140, 1800, 2940, 2880, 3960]
    assert sum(actual_signal_strengths) == 13140
