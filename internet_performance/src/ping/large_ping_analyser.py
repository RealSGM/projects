def main():
    with open('large_ping.txt') as f:
        lines = f.readlines()
        last_line = lines[-1]
        second_last_line = lines[-2]
        
        # extract packet loss from second last line
        packet_loss = second_last_line.split(' ')[-5]
        # extract average rtt from last line
        avg_rtt = last_line.split(' ')[3].split('/')[1]
        
        print(f'Packet loss: {packet_loss}')
        print(f'Average RTT: {avg_rtt} ms')

if __name__ == '__main__':
    main()