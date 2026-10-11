import sys
import time

def run_catscript(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"[Error]: File '{file_path}' not found! Please check the path.")
        return

    belly = 0
    memory = 0
    
    lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith(';')]
    
    ip = 0  
    last_if_status = True  
    while_stack = []

    while ip < len(lines):
        line = lines[ip]
        
        time.sleep(0.005)
        
        if not last_if_status and not (line == "EarsBack" or line == "TailDown"):
            ip += 1
            continue

        if line == "Meow":
            belly += 1
        elif line == "Hiss":
            belly -= 1
        elif line == "MeowMeowMeow":
            belly += 10
        elif line == "HissHissHiss":
            belly -= 10
        elif line == "Tygydyk":
            belly *= 2
        elif line == "Share":
            belly //= 2
        elif line == "Churu":
            belly *= 5
        elif line == "Drop":
            belly = 0
        elif line == "Puke":
            belly, memory = 0, 0
        elif line == "Bite":
            print("\n[Cat Status]: The cat bit your finger! Program gracefully stopped.")
            sys.exit(0)
        elif line == "Purr":
            print(chr(belly), end="")
        elif line == "Scream":
            print(f"\n[Belly Value]: {belly}")
        elif line == "Stare":
            user_input = sys.stdin.read(1)
            belly = ord(user_input) if user_input else 0
        elif line == "Sniff":
            try:
                belly = int(input("\n[Cat Needs Number]: "))
            except ValueError:
                belly = 0
        elif line == "Burry":
            memory = belly
        elif line == "DigOut":
            belly = memory
        elif line == "EyesWide":
            last_if_status = (belly > 0)
        elif line == "EarsBack":
            last_if_status = not last_if_status
        elif line == "TailUp":
            if belly != 0:
                if not while_stack or while_stack[-1] != ip:
                    while_stack.append(ip)
            else:
                scan_ip = ip
                depth = 0
                while scan_ip < len(lines):
                    if lines[scan_ip] == "TailUp": depth += 1
                    if lines[scan_ip] == "TailDown": depth -= 1
                    if depth == 0: break
                    scan_ip += 1
                ip = scan_ip
        elif line == "TailDown":
            if while_stack:
                ip = while_stack[-1] - 1
            else:
                print("[Cat Error]: TailDown without TailUp!")
                sys.exit(1)
        elif line == "Sleep":
            time.sleep(5)  
        elif line == "Lick":
            pass  
        elif line == "LaserPointer":
            ip += 5
            continue
        elif line == "ChaseTail":
            ip -= 5
            continue
        else:
            print(f"\n[Cat Error]: The cat ignored the unknown action '{line}'")
            sys.exit(1)

        ip += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python catscript.py <filename.cat>")
    else:
        run_catscript(sys.argv[1])
