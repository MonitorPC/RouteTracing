# Route tracing

This Python code uses the `scapy` library to perform a custom traceroute to a specified target IP address. Here's a breakdown of how to use it:

**1. Prerequisites:**

* **Install Python:**  Make sure you have Python installed on your system.
* **Install Scapy:** Open your terminal or command prompt and run:
   ```bash
   pip install scapy
   ```

**2. Running the Script:**

* **Save the code:** Save the code as a Python file (e.g., `traceroute.py`).
* **Open your terminal or command prompt.**
* **Run the script:** Use the following command structure:

   ```bash
   python traceroute.py <target_ip> [options]
   ```

   * **`<target_ip>`:**  Replace with the actual IP address or domain name you want to trace the route to (e.g., `8.8.8.8` or `google.com`).
   * **[options]:** (Optional)
      * `-p <protocol>`: Specify the network protocol to use (default: ICMP).
         * `I`: ICMP
         * `T`: TCP
         * `U`: UDP
      * `-m <max_hops>`: Set the maximum number of hops (default: 30).
      * `-t <timeout>`:  Set the timeout in seconds for each hop (default: 2.0).
      * `-v`: Enable verbose mode for detailed output.

**Examples:**

* **Basic traceroute using ICMP:**
   ```bash
   python traceroute.py 8.8.8.8 
   ```

* **Traceroute using TCP with a maximum of 20 hops:**
   ```bash
   python traceroute.py google.com -p T -m 20
   ```

* **Traceroute with verbose output:**
   ```bash
   python traceroute.py 192.168.1.1 -v
   ```

**Understanding the Output:**

The script will print each hop number, the IP address and hostname (if resolvable) of the hop, and the round-trip time (RTT).  If a hop times out, you'll see `* * * Timeout`. 

**How it Works:**

* **Imports:** The code starts by importing necessary modules (`scapy`, `sys`, `time`, `argparse`, `socket`).
* **Argument Parsing:**  It uses `argparse` to handle command-line arguments, allowing you to customize the traceroute.
* **Protocol Functions:** The `udp`, `tcp`, and `icmp` functions construct and send packets using the specified protocol and handle the responses.
* **Main Loop:** The main part of the script iterates through the hop count, sending packets and printing the results until it reaches the target IP or the maximum hop count.

**Key Points:**

* **Scapy:**  Scapy is a powerful packet manipulation library that allows you to create, send, receive, and analyze network packets.
* **Traceroute Logic:** The code implements the basic traceroute logic by incrementing the Time-To-Live (TTL) value of the sent packets, causing routers along the path to respond.
* **Protocol Options:** You can choose different protocols (ICMP, TCP, UDP) to see if certain hops behave differently.

Let me know if you have any more questions! 
