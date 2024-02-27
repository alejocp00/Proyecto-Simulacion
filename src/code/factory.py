import heapq
from platform import machine
from threading import Thread
import time
from queue import Queue

from src.code.machines import Machine
from src.code.auxiliar_functions import get_repair_time

class Factory:
    def __init__(self, n:int, s:int):
        self.n = n
        self.s = s
        self.__populate_factory()
        self.__broken_machines = Queue()
        self.__crashed = False
        
    def start_factory(self):
        self.__repair_thread = Thread(target=self.__repair_machine)
        self.__repair_thread.start()
        
        self.__run_all_machines()
        
        self.__check_machines_state()
        
        self.__factory_crashed()

    def __run_all_machines(self):
        for (_,machine) in self.__working_machines:
            machine.start_working()
            
    def __populate_factory(self):
        self.__working_machines = []
        self.__idle_machines = Queue()
        for i in range(self.s):
            machine = Machine(self.n+i)
            self.__idle_machines.put(machine)
        
        heapq.heapify(self.__working_machines)
        
        for i in range(self.n):
            machine = Machine(i)
            heapq.heappush(self.__working_machines, (machine.get_work_time(), machine))
            
    def __repair_machine(self):
        while not self.__crashed:
            if not self.__broken_machines.empty():
                machine = self.__broken_machines.get()
                time.sleep(get_repair_time())
                self.__idle_machines.put(machine)
                
    def __check_machines_state(self):
        _,machine = heapq.heappop(self.__working_machines)
        while True:
            if machine.get_start_time() + machine.get_work_time() < time.time():
                
                # Check if there are available machines to replace the broken one
                if self.__idle_machines.empty():
                    break
                
                self.__swap_machine(machine)
                
                _,machine = heapq.heappop(self.__working_machines)
            
                
    def __swap_machine(self, machine):
        new_machine = self.__idle_machines.get()
        new_machine.start_working()
        heapq.heappush(self.__working_machines, (new_machine.get_work_time(), new_machine))

        
    def __factory_crashed(self):
        print("The factory has crashed")
        self.__crashed = True
        self.__repair_thread.join()