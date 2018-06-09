--Copyright (C) 2016 Siavoosh Payandeh Azad

library ieee;
use ieee.std_logic_1164.all;
--use IEEE.STD_LOGIC_ARITH.ALL;
--use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity FIFO_credit_based_with_checkers is
    generic (
        DATA_WIDTH: integer := 32
    );
    port (  reset: in std_logic;
            clk  : in std_logic;
            RX   : in std_logic_vector (DATA_WIDTH-1 downto 0); 
            valid_in  : in  std_logic;
            read_en_N : in  std_logic;
            read_en_E : in  std_logic;
            read_en_W : in  std_logic;
            read_en_S : in  std_logic;
            read_en_L : in  std_logic;
            hold_in_from_allocator: in std_logic;

            credit_out: out std_logic; -- acts as hold_out too ?!
            empty_out : out std_logic; 
            Data_out  : out std_logic_vector (DATA_WIDTH-1 downto 0); 
            hold_out: out std_logic
    );
end FIFO_credit_based_with_checkers;

architecture behavior of FIFO_credit_based_with_checkers is

  component FIFO_credit_based_checkers is
      port (  valid_in  : in  std_logic;
              read_en_N : in  std_logic;
              read_en_E : in  std_logic;
              read_en_W : in  std_logic;
              read_en_S : in  std_logic;
              read_en_L : in  std_logic;
              read_pointer: in std_logic_vector(3 downto 0);
              read_pointer_in: in std_logic_vector(3 downto 0);
              write_pointer: in std_logic_vector(3 downto 0);
              write_pointer_in: in std_logic_vector(3 downto 0);
              full: in std_logic; 
              empty: in std_logic;
              read_en: in std_logic;
              write_en: in std_logic;

              -- FIFO Control Part Checkers Output
              FIFO_checkers_output: out std_logic
      );
  end component;

   signal read_pointer, read_pointer_in,  write_pointer, write_pointer_in: std_logic_vector(3 downto 0);
   signal full, empty: std_logic;
   signal read_en, write_en: std_logic;

   signal FIFO_MEM_1, FIFO_MEM_1_in : std_logic_vector(DATA_WIDTH-1 downto 0);
   signal FIFO_MEM_2, FIFO_MEM_2_in : std_logic_vector(DATA_WIDTH-1 downto 0);
   signal FIFO_MEM_3, FIFO_MEM_3_in : std_logic_vector(DATA_WIDTH-1 downto 0);
   signal FIFO_MEM_4, FIFO_MEM_4_in : std_logic_vector(DATA_WIDTH-1 downto 0);

   signal credit: std_logic;

   -- Checkers output related signals used for AWAT!
   signal FIFO_checkers_output, FIFO_checkers_output_sync: std_logic; 

begin

 --------------------------------------------------------------------------------------------
--                           block diagram of the FIFO!


 --------------------------------------------------------------------------------------------
--  circular buffer structure
--                                   <--- WriteP    
--              ---------------------------------
--              |   3   |   2   |   1   |   0   |
--              ---------------------------------
--                                   <--- readP   
 --------------------------------------------------------------------------------------------

-----------------------------------------------------------------------
-----------------------------------------------------------------------

  -- FIFO control part checkers instantiation
  FIFO_CONTROL_PART_CHECKERS: FIFO_credit_based_checkers port map 
                                          (
                                            valid_in  => valid_in, 
                                            read_en_N => read_en_N, 
                                            read_en_E => read_en_E, 
                                            read_en_W => read_en_W, 
                                            read_en_S => read_en_S, 
                                            read_en_L => read_en_L, 
                                            read_pointer => read_pointer, 
                                            read_pointer_in => read_pointer_in, 
                                            write_pointer => write_pointer, 
                                            write_pointer_in => write_pointer_in, 
                                            full => full, 
                                            empty => empty, 
                                            read_en => read_en, 
                                            write_en => write_en, 

                                            FIFO_checkers_output => FIFO_checkers_output
                                          );

-----------------------------------------------------------------------
-----------------------------------------------------------------------

   -- Sequential part

   process (clk, reset) begin
        if reset = '0' then
            read_pointer  <= "0001";
            write_pointer <= "0001";

            FIFO_MEM_1 <= (others=>'0');
            FIFO_MEM_2 <= (others=>'0');
            FIFO_MEM_3 <= (others=>'0');
            FIFO_MEM_4 <= (others=>'0');

            credit <= '0';

        elsif clk'event and clk = '1' then

          if FIFO_checkers_output_sync = '0' then
            write_pointer <= write_pointer_in;
            read_pointer  <=  read_pointer_in;
          end if;
          if hold_in_from_allocator = '0' and credit = '1' then
            credit <= '0'; 
          end if;  
          if FIFO_checkers_output_sync = '0' and hold_in_from_allocator = '0' then         
            if write_en = '1' then 
                --write into the memory
                  FIFO_MEM_1 <= FIFO_MEM_1_in;
                  FIFO_MEM_2 <= FIFO_MEM_2_in;
                  FIFO_MEM_3 <= FIFO_MEM_3_in;
                  FIFO_MEM_4 <= FIFO_MEM_4_in;                   
            end if;
          end if;
          if FIFO_checkers_output_sync = '0' then
            if read_en = '1' then 
              credit <= '1';
            end if;
          end if;

        end if;
    end process;

    -- AWAIT-related logic (Sequential)
    process(FIFO_checkers_output, clk)
    begin
          if FIFO_checkers_output = '1' then -- If there is a transient fault detected in FIFO control part
                FIFO_checkers_output_sync <= '1';
          else -- Hopefully the transient fault would disappear 
                if clk'event and clk = '0' then 
                      FIFO_checkers_output_sync <= '0';
                end if;
          end if; 
    end process;

-----------------------------------------------------------------------
-----------------------------------------------------------------------
 
   -- The combionational part

   -- AWAIT-related logic




   -- FIFO-related logic

   credit_out <= credit;

   process(RX, write_pointer, FIFO_MEM_1, FIFO_MEM_2, FIFO_MEM_3, FIFO_MEM_4) begin
      case( write_pointer ) is
          when "0001" => FIFO_MEM_1_in <= RX;         FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
          when "0010" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= RX;         FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
          when "0100" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= RX;         FIFO_MEM_4_in <= FIFO_MEM_4; 
          when "1000" => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= RX;                  
          when others => FIFO_MEM_1_in <= FIFO_MEM_1; FIFO_MEM_2_in <= FIFO_MEM_2; FIFO_MEM_3_in <= FIFO_MEM_3; FIFO_MEM_4_in <= FIFO_MEM_4; 
      end case ;
   end process;

  process(read_pointer, FIFO_MEM_1, FIFO_MEM_2, FIFO_MEM_3, FIFO_MEM_4) begin
    case( read_pointer ) is
        when "0001" => Data_out <= FIFO_MEM_1;
        when "0010" => Data_out <= FIFO_MEM_2;
        when "0100" => Data_out <= FIFO_MEM_3;
        when "1000" => Data_out <= FIFO_MEM_4;
        when others => Data_out <= FIFO_MEM_1; 
    end case ;
  end process;

  read_en   <= (read_en_N or read_en_E or read_en_W or read_en_S or read_en_L) and not empty; 
  empty_out <= empty or FIFO_checkers_output_sync or hold_in_from_allocator; -- ?!
  hold_out  <= FIFO_checkers_output_sync or hold_in_from_allocator; 

  process(write_en, write_pointer) begin
    if write_en = '1'then
       write_pointer_in <= write_pointer(2 downto 0) & write_pointer(3); 
    else
       write_pointer_in <= write_pointer; 
    end if;
  end process;

  process(read_en, empty, read_pointer) begin
       if (read_en = '1' and empty = '0') then
           read_pointer_in <= read_pointer(2 downto 0) & read_pointer(3); 
       else 
           read_pointer_in <= read_pointer; 
       end if;
  end process;

  process(full, valid_in) begin
     if valid_in = '1' and full ='0' then
         write_en <= '1';
     else
         write_en <= '0';
     end if;        
  end process;
                        
  process(write_pointer, read_pointer) begin
      if read_pointer = write_pointer then
              empty <= '1';
      else
              empty <= '0';
      end if;
      --      if write_pointer = read_pointer>>1 then
      if write_pointer = read_pointer(0) & read_pointer(3 downto 1) then
              full <= '1';
      else
              full <= '0'; 
      end if; 
  end process;

end;