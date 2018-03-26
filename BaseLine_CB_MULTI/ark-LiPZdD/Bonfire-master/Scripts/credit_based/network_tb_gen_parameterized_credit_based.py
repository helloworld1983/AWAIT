# Copyright (C) 2016 Siavoosh Payandeh Azad

from math import ceil, log
import random

# -D [size]: sets the size of the network, it can be powers of two
# -Rand: generates random traffic patterns

import sys


if '--help' in sys.argv[1:]:
  print "\t-D [network size]: makes a test bench for network of [size]X[size]. Size can be "
  print "\t                   only multiples of two. default value is 4."
  print "\t-DW [data_width]: sets the data width of the network!"
  print "\t[-Rand/-BR] [PIR]: Uses [Rand]om traffic pattern generator with packet injection rate equal to PIR"
  print "\t                   or Uses [B]it[R]eversal traffic pattern generator with packet injection rate equal to PIR"
  print "\t                   default case is repetitive packets being sent from source to same destination"
  print "\t-o: specifies the name and path of the output file. default path is current folder!"
  print "\t-PS [min packet size] [max packet size]: specifies packet size. default min value is 3 and default max value is 8."
  print "\t-PE: adds processing elements in each node"
  print "\t-SHMU: maps shmu on one of the nodes"
  print "\t-NI_Test: adds an NI to the nodes and connects a traffic generator to it"
  print "\t-trace: adds trackers to network outputs"
  print "\t-sim: specifies the length of simulation in clock cycles. which at this time the packet generators will stop sending packets."
  print "\t-verbal: prints more details"
  print "\t**Example 1: python network_tb_gen_parameterized_credit_based.py -D 2 -SHMU -NI_Test -Rand 0.01 -PS 3 3 -sim 10000 "
  print "\t           generates a testbench for a 2X2 network and adds NIs and NI_Testers to it which sends packets to random destinations "
  print "\t           with 0.01 injection rate, and packet size of 3 until 10000 ns"
  print "\t**Example 2: python network_tb_gen_parameterized_credit_based.py -D 2 -Rand 0.005 -PS 3 3 -sim 10000  "
  print "\t           generates a testbench for a 2X2 network which uses random traffic pattern generator with PIR of 0.005 and fixed"
  print "\t           packet size of 3 and sends packets until 10000 ns"
  sys.exit()

network_dime = 4
data_width = 32
random_dest = False
add_tracker = False
add_SHMU = False
add_node = False
add_NI_Test = False
got_finish_time = False
sim_finish_time = None
bit_reversal = False
get_packet_size = False
packet_size_min = 3
packet_size_max = 8
verbal = False
# file_path = file_name+'_'+str(network_dime)+"x"+str(network_dime)+'.vhd'

if '-D'  in sys.argv[1:]:
  network_dime = int(sys.argv[sys.argv.index('-D')+1])


if '-DW' in sys.argv[1:]:
  data_width = int(sys.argv[sys.argv.index('-DW')+1])
  if data_width % 2 != 0:
    raise ValueError("wrong data width. please choose powers of 2. for example 32!")

if '-Rand'  in sys.argv[1:]:
  random_dest = True
  PIR = float(sys.argv[sys.argv.index('-Rand')+1])
  frame_size = int(ceil(1.0/PIR))

if '-SHMU'  in sys.argv[1:]:
    add_SHMU = True

if '-NI_Test' in sys.argv[1:]:
    add_NI_Test = True

if "-PE" in sys.argv[1:]:
  add_node = True

if "-trace" in sys.argv[1:]:
  add_tracker = True

if '-BR'  in sys.argv[1:]:
  bit_reversal = True
  PIR = float(sys.argv[sys.argv.index('-BR')+1])
  frame_size = int(ceil(1.0/PIR))


if random_dest and bit_reversal:
  raise ValueError("Can not accept multiple traffic patterns at the same time...")

if '-sim'  in sys.argv[1:]:
  got_finish_time = True
  sim_finish_time = int(sys.argv[sys.argv.index('-sim')+1])


if '-PS'  in sys.argv[1:]:
  get_packet_size = True
  packet_size_min = int(sys.argv[sys.argv.index('-PS')+1])
  packet_size_max = int(sys.argv[sys.argv.index('-PS')+2])

if '-verbal' in sys.argv[1:]:
  verbal = True

file_name = 'tb_network'
if random_dest:
  file_name += '_rand'
elif bit_reversal:
  file_name += '_br'

if '-o'  in sys.argv[1:]:
  file_path = sys.argv[sys.argv.index('-o')+1]
  if ".vhd" not in file_path:
      raise ValueError("wrong file extention. only vhdl files are accepted!")
else:
  file_path = file_name+'_'+str(network_dime)+"x"+str(network_dime)+'.vhd'

noc_file = open(file_path, 'w')

if add_NI_Test and add_node:
  raise ValueError("cant have -NI_Test and -PE at the same time")

noc_file.write("--Copyright (C) 2016 Siavoosh Payandeh Azad\n")
noc_file.write("------------------------------------------------------------\n")
noc_file.write("-- This file is automatically generated Please do not change!\n")
noc_file.write("-- Here are the parameters:\n")
noc_file.write("-- \t network size x:"+str(network_dime)+"\n")
noc_file.write("-- \t network size y:"+str(network_dime)+"\n")
noc_file.write("-- \t data width:"+str(data_width))
noc_file.write("-- \t traffic pattern:"+str())
noc_file.write("------------------------------------------------------------\n\n")

noc_file.write("library ieee;\n")
noc_file.write("use ieee.std_logic_1164.all;\n")
noc_file.write("use IEEE.STD_LOGIC_ARITH.ALL;\n")
noc_file.write("use IEEE.STD_LOGIC_UNSIGNED.ALL;\n")
noc_file.write("use work.TB_Package.all;\n\n")
noc_file.write("USE ieee.numeric_std.ALL; \n")
noc_file.write("use IEEE.math_real.\"ceil\";\n")
noc_file.write("use IEEE.math_real.\"log2\";\n\n")

noc_file.write("entity tb_network_"+str(network_dime)+"x"+str(network_dime)+" is\n")

noc_file.write("end tb_network_"+str(network_dime)+"x"+str(network_dime)+"; \n")


noc_file.write("\n\n")
noc_file.write("architecture behavior of tb_network_"+str(network_dime)+"x"+str(network_dime)+" is\n\n")

noc_file.write("-- Declaring network component\n")



string_to_print = ""
noc_file.write("component network_"+str(network_dime)+"x"+str(network_dime)+" is\n")

noc_file.write(" generic (DATA_WIDTH: integer := 32; DATA_WIDTH_LV: integer := 11);\n")
noc_file.write("port (reset: in  std_logic; \n")
noc_file.write("\tclk: in  std_logic; \n")
if not add_SHMU:
  noc_file.write("\tRxy_reconf: in  std_logic_vector(7 downto 0);\n")
  noc_file.write("\tReconfig : in std_logic;\n")
for i in range(network_dime**2):
    noc_file.write("\t--------------\n")
    noc_file.write("\tRX_L_"+str(i)+": in std_logic_vector (DATA_WIDTH-1 downto 0);\n")
    noc_file.write("\tcredit_out_L_"+str(i)+", valid_out_L_"+str(i)+": out std_logic;\n")
    noc_file.write("\tcredit_in_L_"+str(i)+", valid_in_L_"+str(i)+": in std_logic;\n")
    if i == network_dime**2-1 and add_SHMU== False:
        noc_file.write("\tTX_L_"+str(i)+": out std_logic_vector (DATA_WIDTH-1 downto 0)\n")
    else:
        noc_file.write("\tTX_L_"+str(i)+": out std_logic_vector (DATA_WIDTH-1 downto 0);\n")


if add_SHMU:
  for i in range(0, network_dime**2):
      string_to_print +="\t--------------\n"
      string_to_print +="    link_faults_"+str(i) +": out std_logic_vector(4 downto 0);\n"
      string_to_print +="    turn_faults_"+str(i) +": out std_logic_vector(19 downto 0);\n"
      string_to_print +="    Rxy_reconf_PE_"+str(i) +": in  std_logic_vector(7 downto 0);\n"
      string_to_print +="    Cx_reconf_PE_"+str(i) +": in  std_logic_vector(3 downto 0);\n"
      string_to_print +="    Reconfig_command_"+str(i) +" : in std_logic;\n\n"

noc_file.write(string_to_print[:len(string_to_print)-3])
noc_file.write("\n            ); \n")
noc_file.write("end component; \n")


if add_tracker:
      noc_file.write("component flit_tracker is\n")
      noc_file.write("    generic (\n")
      noc_file.write("        DATA_WIDTH: integer := 32;\n")
      noc_file.write("        tracker_file: string :=\"track.txt\"\n")
      noc_file.write("    );\n")
      noc_file.write("    port (\n")
      noc_file.write("        clk: in std_logic;\n")
      noc_file.write("        RX: in std_logic_vector (DATA_WIDTH-1 downto 0); \n")
      noc_file.write("        valid_in : in std_logic \n")
      noc_file.write("    );\n")
      noc_file.write("end component;\n")

if add_node and not add_SHMU and not add_NI_Test:
  noc_file.write("component NoC_Node is\n")
  noc_file.write("generic( current_address : integer := 0; stim_file: string :=\"code.txt\";\n")
  noc_file.write("\tlog_file  : string := \"output.txt\");\n\n")

  noc_file.write("port( reset        : in std_logic;\n")
  noc_file.write("      clk          : in std_logic;\n")
  noc_file.write("      \n")
  noc_file.write("        credit_in : in std_logic;\n")
  noc_file.write("        valid_out: out std_logic;\n")
  noc_file.write("        TX: out std_logic_vector(31 downto 0);\n")
  noc_file.write("\n")
  noc_file.write("        credit_out : out std_logic;\n")
  noc_file.write("        valid_in: in std_logic;\n")
  noc_file.write("        RX: in std_logic_vector(31 downto 0)\n")
  noc_file.write("   );\n")
  noc_file.write("end component; --component NoC_Node\n")
elif add_node and add_SHMU and not add_NI_Test:

  noc_file.write("-- Declaring Node component\n\n")
  noc_file.write("component NoC_Node is\n")
  noc_file.write("generic( current_address : integer := 0;\n")
  noc_file.write("         stim_file: string :=\"code.txt\";\n")
  noc_file.write("         log_file  : string := \"output.txt\");\n")
  noc_file.write("\n")
  noc_file.write("port( reset        : in std_logic;\n")
  noc_file.write("      clk          : in std_logic;\n")
  noc_file.write("\n")
  noc_file.write("        credit_in : in std_logic;\n")
  noc_file.write("        valid_out: out std_logic;\n")
  noc_file.write("        TX: out std_logic_vector(31 downto 0);\n")
  noc_file.write("\n")
  noc_file.write("        credit_out : out std_logic;\n")
  noc_file.write("        valid_in: in std_logic;\n")
  noc_file.write("        RX: in std_logic_vector(31 downto 0);\n")
  noc_file.write("\n")
  noc_file.write("        link_faults: in std_logic_vector(4 downto 0);\n")
  noc_file.write("        turn_faults: in std_logic_vector(19 downto 0);\n")
  noc_file.write("\n")
  noc_file.write("        Rxy_reconf_PE: out  std_logic_vector(7 downto 0);\n")
  noc_file.write("        Cx_reconf_PE: out  std_logic_vector(3 downto 0);\n")
  noc_file.write("        Reconfig_command : out std_logic\n")
  noc_file.write("\n")
  noc_file.write("   );\n")
  noc_file.write("end component; --component NoC_Node\n")
elif not add_node and add_SHMU and add_NI_Test:
  noc_file.write("-- Declaring NI component\n\n")
  noc_file.write("component NI is\n")
  noc_file.write("   generic(current_address : integer := 10;   -- the current node's address\n")
  noc_file.write("           SHMU_address : integer := 0); \n")
  # noc_file.write("           reserved_address : std_logic_vector(29 downto 0) := \"000000000000000001111111111111\";\n")
  # noc_file.write("           flag_address : std_logic_vector(29 downto 0) :=     \"000000000000000010000000000000\";  -- reserved address for the memory mapped I/O\n")
  # noc_file.write("           counter_address : std_logic_vector(29 downto 0) :=     \"000000000000000010000000000001\";\n")
  # noc_file.write("           reconfiguration_address : std_logic_vector(29 downto 0) :=     \"000000000000000010000000000010\";  -- reserved address for reconfiguration register\n")
  # noc_file.write("           self_diagnosis_address : std_logic_vector(29 downto 0) :=     \"000000000000000010000000000011\"); -- reserved address for self diagnosis register\n")
  noc_file.write("   port(clk               : in std_logic;\n")
  noc_file.write("        reset             : in std_logic;\n")
  noc_file.write("        enable            : in std_logic;\n")
  noc_file.write("        write_byte_enable : in std_logic_vector(3 downto 0);\n")
  noc_file.write("        address           : in std_logic_vector(31 downto 2);\n")
  noc_file.write("        data_write        : in std_logic_vector(31 downto 0);\n")
  noc_file.write("        data_read         : out std_logic_vector(31 downto 0);\n")
  noc_file.write("\n")
  noc_file.write("        -- Flags used by JNIFR and JNIFW instructions\n")
  noc_file.write("        --NI_read_flag      : out  std_logic;   -- One if the N2P fifo is empty. No read should be performed if one.\n")
  noc_file.write("        --NI_write_flag      : out  std_logic;  -- One if P2N fifo is full. no write should be performed if one.\n")
  noc_file.write("        -- interrupt signal: generated evertime a packet is recieved!\n")
  noc_file.write("        irq_out           : out std_logic;\n")
  noc_file.write("        -- signals for sending packets to network\n")
  noc_file.write("        credit_in : in std_logic;\n")
  noc_file.write("        valid_out: out std_logic;\n")
  noc_file.write("        TX: out std_logic_vector(31 downto 0);  -- data sent to the NoC\n")
  noc_file.write("        -- signals for reciving packets from the network\n")
  noc_file.write("        credit_out : out std_logic;\n")
  noc_file.write("        valid_in: in std_logic;\n")
  noc_file.write("        RX: in std_logic_vector(31 downto 0); -- data recieved form the NoC\n")
  noc_file.write("        -- fault information signals from the router\n")
  noc_file.write("        link_faults: in std_logic_vector(4 downto 0);\n")
  noc_file.write("        turn_faults: in std_logic_vector(19 downto 0);\n")
  noc_file.write("\n")
  noc_file.write("        Rxy_reconf_PE: out  std_logic_vector(7 downto 0);\n")
  noc_file.write("        Cx_reconf_PE: out  std_logic_vector(3 downto 0);    -- if you are not going to update Cx you should write all ones! (it will be and will the current Cx bits)\n")
  noc_file.write("        Reconfig_command : out std_logic\n")
  noc_file.write("  );\n")
  noc_file.write("end component; --component NI\n")

noc_file.write("\n")
noc_file.write("-- generating bulk signals...\n")
for i in range(0, network_dime*network_dime):
    noc_file.write("\tsignal RX_L_"+str(i)+", TX_L_"+str(i)+":  std_logic_vector ("+str(data_width-1)+" downto 0);\n")
    noc_file.write("\tsignal credit_counter_out_"+str(i)+":  std_logic_vector (1 downto 0);\n")
    noc_file.write("\tsignal credit_out_L_"+str(i)+", credit_in_L_"+str(i)+", valid_in_L_"+str(i)+", valid_out_L_"+str(i) + ": std_logic;\n")

#noc_file.write("\n\nAlias buried_sig is <<signal .NoC.valid_in_E_11 :std_logic>>;\n\n")

if add_SHMU:
  for i in range(0, network_dime*network_dime):
    noc_file.write("\tsignal link_faults_"+str(i)+ " : std_logic_vector(4 downto 0);\n")
    noc_file.write("\tsignal turn_faults_"+str(i)+ " : std_logic_vector(19 downto 0);\n")
    noc_file.write("\tsignal Rxy_reconf_PE_"+str(i)+ " : std_logic_vector(7 downto 0);\n")
    noc_file.write("\tsignal Cx_reconf_PE_"+str(i)+ " : std_logic_vector(3 downto 0);\n")
    noc_file.write("\tsignal Reconfig_command_"+str(i)+ " : std_logic;\n")

noc_file.write("\t-- NI testing signals\n")
if add_NI_Test:

  noc_file.write("\tsignal reserved_address :        std_logic_vector(29 downto 0):= \"000000000000000001111111111111\";\n")
  noc_file.write("\tsignal flag_address :            std_logic_vector(29 downto 0):= \"000000000000000010000000000000\" ; -- reserved address for the memory mapped I/O\n")
  noc_file.write("\tsignal counter_address :         std_logic_vector(29 downto 0):= \"000000000000000010000000000001\";\n")
  noc_file.write("\tsignal reconfiguration_address : std_logic_vector(29 downto 0):= \"000000000000000010000000000010\";  -- reserved address for reconfiguration register\n")
  noc_file.write("\tsignal self_diagnosis_address :  std_logic_vector(29 downto 0):= \"000000000000000010000000000011\";\n")

  string_to_print = ""
  for i in range(0, network_dime*network_dime):
    string_to_print += "irq_out_"+str(i)+ ", "
  noc_file.write("\tsignal "+string_to_print[:-2]+": std_logic;\n")

  string_to_print = ""
  for i in range(0, network_dime*network_dime):
    string_to_print += "test_"+str(i)+ ", "
  noc_file.write("\tsignal "+string_to_print[:-2]+": std_logic_vector(31 downto 0);\n")

  string_to_print = ""
  for i in range(0, network_dime*network_dime):
    string_to_print += "enable_"+str(i)+ ", "
  noc_file.write("\tsignal "+string_to_print[:-2]+": std_logic;\n")
  string_to_print = ""
  for i in range(0, network_dime*network_dime):
    string_to_print += "write_byte_enable_"+str(i)+ ", "
  noc_file.write("\tsignal "+string_to_print[:-2]+": std_logic_vector(3 downto 0);\n")
  string_to_print = ""
  for i in range(0, network_dime*network_dime):
    string_to_print += "address_"+str(i)+ ", "
  noc_file.write("\tsignal "+string_to_print[:-2]+": std_logic_vector(31 downto 2);\n")
  string_to_print = ""
  for i in range(0, network_dime*network_dime):
    string_to_print += "data_write_"+str(i)+ ", "
  noc_file.write("\tsignal "+string_to_print[:-2]+": std_logic_vector(31 downto 0);\n")
  string_to_print = ""
  for i in range(0, network_dime*network_dime):
    string_to_print += "data_read_"+str(i)+ ", "
  noc_file.write("\tsignal "+string_to_print[:-2]+": std_logic_vector(31 downto 0);\n")



noc_file.write("\t--------------\n")
if not add_SHMU:
  noc_file.write("\tsignal Rxy_reconf: std_logic_vector (7 downto 0) := \"01111101\";\n")
  noc_file.write("\tsignal Reconfig: std_logic := '0';\n")

noc_file.write("\t--------------\n")
noc_file.write("\tconstant clk_period : time := 10 ns;\n")
noc_file.write("\tsignal reset, not_reset, clk: std_logic :='0';\n")

noc_file.write("\n")
noc_file.write("begin\n\n")


noc_file.write("   clk_process :process\n")
noc_file.write("   begin\n")
noc_file.write("        clk <= '0';\n")
noc_file.write("        wait for clk_period/2;   \n")
noc_file.write("        clk <= '1';\n")
noc_file.write("        wait for clk_period/2; \n")
noc_file.write("   end process;\n")
noc_file.write("\n")
noc_file.write("reset <= '1' after 1 ns;\n")

noc_file.write("-- instantiating the network\n")


if add_tracker:
    noc_file.write("-- instantiating the flit trackers\n")
    for i in range(0, network_dime**2):
        noc_file.write("F_T_"+str(i)+"_T: flit_tracker  generic map (\n")
        noc_file.write("        DATA_WIDTH => "+str(data_width)+", \n")
        noc_file.write("        tracker_file =>\"traces/track"+str(i)+"_T.txt\"\n")
        noc_file.write("    )\n")
        noc_file.write("    port map (\n")
        noc_file.write("        clk => clk, RX => TX_L_"+str(i)+", \n")
        noc_file.write("        valid_in => valid_out_L_"+str(i)+"\n")
        noc_file.write("    );\n")


string_to_print = ""
string_to_print += "NoC: network_"+str(network_dime)+"x"+str(network_dime)+" generic map (DATA_WIDTH  => "+str(data_width)+", DATA_WIDTH_LV => 11)\n"
if not add_SHMU:
  string_to_print += "port map (reset, clk, Rxy_reconf, Reconfig, \n"
else:
  string_to_print += "port map (reset, clk, \n"

for i in range(network_dime**2):
    string_to_print += "\tRX_L_"+str(i)+", credit_out_L_"+str(i)+", valid_out_L_"+str(i)+", credit_in_L_"+str(i)+", valid_in_L_"+str(i)+",  TX_L_"+str(i)+", \n"

if add_SHMU:
    string_to_print += "\t-- should be connected to NI\n"
    for i in range(0, network_dime**2):
      string_to_print += "\tlink_faults_"+str(i)+", turn_faults_"+str(i)+","
      string_to_print += "\tRxy_reconf_PE_"+str(i)+", Cx_reconf_PE_"+str(i)+", Reconfig_command_"+str(i)+", \n"

noc_file.write(string_to_print[:len(string_to_print)-3])
noc_file.write("\n            ); \n")


noc_file.write("not_reset <= not reset; \n")


if add_node and not add_SHMU and not add_NI_Test:
  noc_file.write("\n")
  noc_file.write("-- connecting the PEs\n")

  for node_number in range(0, network_dime*network_dime):

      noc_file.write("PE_" + str(node_number) + ": NoC_Node \n")

      noc_file.write("generic map( current_address => " + str(node_number) + ",\n")
      noc_file.write("\tstim_file => \"code_" + str(node_number).zfill(3) + ".txt\",\n")
      noc_file.write("\tlog_file  => \"output_" + str(node_number).zfill(3) + ".txt\")\n\n")

      noc_file.write("port map( not_reset, clk, \n")
      noc_file.write("\n")
      noc_file.write("        credit_in => credit_out_L_" + str(node_number) + ", \n")
      noc_file.write("        valid_out => valid_in_L_" + str(node_number) + ",\n")
      noc_file.write("        TX => RX_L_" + str(node_number) + ", \n")
      noc_file.write("\n")
      noc_file.write("        credit_out => credit_in_L_" + str(node_number) + ", \n")
      noc_file.write("        valid_in => valid_out_L_" + str(node_number) + ",\n")
      noc_file.write("        RX => TX_L_" + str(node_number) + "\n")
      noc_file.write("   );\n")

if add_SHMU and not add_NI_Test:
  noc_file.write("\n")
  noc_file.write("-- connecting the PEs\n")

  for node_number in range(0, network_dime*network_dime):

      noc_file.write("PE_" + str(node_number) + ": NoC_Node \n")

      noc_file.write("generic map( current_address => " + str(node_number) + ",\n")
      noc_file.write("\tstim_file => \"code_" + str(node_number) + ".txt\",\n")
      noc_file.write("\tlog_file  => \"output_" + str(node_number) + ".txt\")\n\n")

      noc_file.write("port map( not_reset, clk, \n")
      noc_file.write("\n")
      noc_file.write("        credit_in => credit_out_L_" + str(node_number) + ", \n")
      noc_file.write("        valid_out => valid_in_L_" + str(node_number) + ",\n")
      noc_file.write("        TX => RX_L_" + str(node_number) + ", \n")
      noc_file.write("\n")
      noc_file.write("        credit_out => credit_in_L_" + str(node_number) + ", \n")
      noc_file.write("        valid_in => valid_out_L_" + str(node_number) + ",\n")
      noc_file.write("        RX => TX_L_" + str(node_number) + ",\n")
      noc_file.write("        link_faults => link_faults_"+str(node_number)+",\n")
      noc_file.write("        turn_faults => turn_faults_"+str(node_number)+",\n")
      noc_file.write("        Rxy_reconf_PE => Rxy_reconf_PE_"+str(node_number)+", \n")
      noc_file.write("        Cx_reconf_PE => Cx_reconf_PE_"+str(node_number)+",\n")
      noc_file.write("        Reconfig_command => Reconfig_command_"+str(node_number)+"\n")
      noc_file.write("   );\n")
elif add_NI_Test and add_SHMU:
    noc_file.write("\n")
    noc_file.write("-- connecting the NIs\n")

    for node_number in range(0, network_dime*network_dime):
      noc_file.write("NI_" + str(node_number) + ": NI \n")
      noc_file.write("   generic map(current_address => " + str(node_number) + "\n")
      noc_file.write("           ) \n")
      noc_file.write("   port map(clk => clk , reset => not_reset , enable => enable_" + str(node_number) + ", \n")
      noc_file.write("        write_byte_enable => write_byte_enable_" + str(node_number) + ", \n")
      noc_file.write("        address => address_" + str(node_number) + ", \n")
      noc_file.write("        data_write => data_write_" + str(node_number) + ", \n")
      noc_file.write("        data_read => data_read_" + str(node_number) + ", \n")
      noc_file.write("        -- interrupt signal: generated evertime a packet is recieved!\n")
      noc_file.write("        irq_out => irq_out_" + str(node_number) + ", \n")
      noc_file.write("        -- signals for sending packets to network\n")
      noc_file.write("        credit_in => credit_out_L_" + str(node_number) + ", \n")
      noc_file.write("        valid_out => valid_in_L_" + str(node_number) + ",\n")
      noc_file.write("        TX => RX_L_" + str(node_number) + ", -- data sent to the NoC\n")
      noc_file.write("        -- signals for reciving packets from the network\n")
      noc_file.write("        credit_out => credit_in_L_" + str(node_number) + ", \n")
      noc_file.write("        valid_in => valid_out_L_" + str(node_number) + ",\n")
      noc_file.write("        RX => TX_L_" + str(node_number) + ",\n")
      noc_file.write("        -- fault information signals from the router\n")
      noc_file.write("        link_faults => link_faults_" + str(node_number) + ", \n")
      noc_file.write("        turn_faults => turn_faults_" + str(node_number) + ",\n")
      noc_file.write("\n")
      noc_file.write("        Rxy_reconf_PE => Rxy_reconf_PE_" + str(node_number) + ", \n")
      noc_file.write("        Cx_reconf_PE => Cx_reconf_PE_" + str(node_number) + ",\n")
      noc_file.write("        Reconfig_command => Reconfig_command_" + str(node_number) + "\n")
      noc_file.write("  );\n")

    noc_file.write("\n\n")
    noc_file.write("-- connecting the packet generators\n")
    for node_number in range(0, network_dime*network_dime):
      random_start = random.randint(3, 50)
      if got_finish_time:
        random_end = sim_finish_time
      else:
        random_end = random.randint(random_start, 200)

      noc_file.write("NI_control("+str(network_dime)+", "+str(frame_size)+", "+str(node_number)+", "+str(random_start)+", " +str(packet_size_min)+", " +str(packet_size_max)+", "+str(random_end)+" ns, clk,\n")
      noc_file.write("           -- NI configuration\n")
      noc_file.write("           reserved_address, flag_address, counter_address, reconfiguration_address, self_diagnosis_address,\n")
      noc_file.write("           -- NI signals\n")
      noc_file.write("           enable_" + str(node_number) + ", write_byte_enable_" + str(node_number) + ", address_" + str(node_number) + ", data_write_" + str(node_number) + ", data_read_" + str(node_number) + ", test_"+str(node_number)+"); \n")
      noc_file.write("\n")
else:
  noc_file.write("\n")
  noc_file.write("-- connecting the packet generators\n")
  if random_dest or bit_reversal:
    for i in range(0, network_dime*network_dime):
      random_start = random.randint(3, 50)
      if got_finish_time:
        random_end = sim_finish_time
      else:
        random_end = random.randint(random_start, 200)

      noc_file.write("credit_counter_control(clk, credit_out_L_"+str(i)+", valid_in_L_"+str(i)+", credit_counter_out_"+str(i)+");\n")

      if random_dest:
        noc_file.write("gen_random_packet("+str(network_dime)+", "+str(frame_size)+", "+str(i)+", "+str(random_start)+", " +str(packet_size_min)+", " +str(packet_size_max)+", " +
                      str(random_end)+" ns, clk, credit_counter_out_"+str(i)+", valid_in_L_"+str(i)+", RX_L_"+str(i)+");\n")
      elif bit_reversal:
        noc_file.write("gen_bit_reversed_packet("+str(network_dime)+", "+str(frame_size)+", "+str(i)+", "+str(random_start)+", " +str(packet_size_min)+", " +str(packet_size_max)+", " +
                      str(random_end)+" ns, clk, credit_counter_out_"+str(i)+", valid_in_L_"+str(i)+", RX_L_"+str(i)+");\n")

      noc_file.write("\n")

if not add_node and not add_NI_Test:
  noc_file.write("\n")
  noc_file.write("-- connecting the packet receivers\n")
  for i in range(0, network_dime*network_dime):
    noc_file.write("get_packet("+str(data_width)+", 5, "+str(i)+", clk, credit_in_L_"+str(i)+", valid_out_L_"+str(i)+", TX_L_"+str(i)+");\n")

noc_file.write("\n\n")

noc_file.write("end;\n")