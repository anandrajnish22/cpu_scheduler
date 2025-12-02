import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import deque

# ------------------ Scheduling Algorithms ------------------

def avg(lst):
    return sum(lst)/len(lst) if lst else 0

# Each algorithm expects processes as list of dicts: {'pid', 'arrival', 'burst', 'priority'}

def fcfs_algo(processes):
    procs = [{**p, 'burst_orig': p['burst']} for p in processes]
    time = 0
    schedule = []
    for p in sorted(procs, key=lambda x: (x['arrival'], x['pid'])):
        if time < p['arrival']:
            time = p['arrival']
        start = time
        time += p['burst']
        end = time
        p['wait'] = start - p['arrival']
        p['tat'] = end - p['arrival']
        schedule.append((start, p['pid'], end))
    return schedule, procs


def sjf_nonpreemptive_algo(processes):
    procs = [{**p, 'burst_orig': p['burst'], 'added': False} for p in processes]
    time = 0
    schedule = []
    completed = 0
    n = len(procs)
    while completed < n:
        ready = [p for p in procs if p['arrival'] <= time and not p.get('done')]
        if not ready:
            time += 1
            continue
        ready.sort(key=lambda x: (x['burst'], x['arrival'], x['pid']))
        cur = ready[0]
        start = time
        time += cur['burst']
        end = time
        cur['done'] = True
        cur['wait'] = start - cur['arrival']
        cur['tat'] = end - cur['arrival']
        schedule.append((start, cur['pid'], end))
        completed += 1
    return schedule, procs


def srtf_algo(processes):
    procs = [{**p, 'burst_rem': p['burst'], 'burst_orig': p['burst']} for p in processes]
    time = 0
    completed = 0
    n = len(procs)
    schedule = []
    last_pid = None
    start_segment = None
    while completed < n:
        ready = [p for p in procs if p['arrival'] <= time and p['burst_rem'] > 0]
        if not ready:
            time += 1
            continue
        cur = min(ready, key=lambda x: (x['burst_rem'], x['arrival'], x['pid']))
        if last_pid != cur['pid']:
            if last_pid is not None:
                schedule.append((start_segment, last_pid, time))
            last_pid = cur['pid']
            start_segment = time
        cur['burst_rem'] -= 1
        time += 1
        if cur['burst_rem'] == 0:
            cur['tat'] = time - cur['arrival']
            cur['wait'] = cur['tat'] - cur['burst_orig']
            completed += 1
    if last_pid is not None:
        schedule.append((start_segment, last_pid, time))
    return schedule, procs


def round_robin_algo(processes, quantum):
    procs = [{**p, 'burst_rem': p['burst'], 'burst_orig': p['burst'], 'finish': None} for p in processes]
    time = 0
    q = deque()
    schedule = []
    added = set()
    while True:
        for p in procs:
            if p['arrival'] <= time and p['pid'] not in added:
                q.append(p); added.add(p['pid'])
        if not q:
            if all(p['burst_rem'] == 0 for p in procs):
                break
            time += 1
            continue
        cur = q.popleft()
        start = time
        run = min(quantum, cur['burst_rem'])
        cur['burst_rem'] -= run
        time += run
        schedule.append((start, cur['pid'], time))
        for p in procs:
            if p['arrival'] <= time and p['pid'] not in added:
                q.append(p); added.add(p['pid'])
        if cur['burst_rem'] > 0:
            q.append(cur)
        else:
            cur['finish'] = time
            cur['tat'] = cur['finish'] - cur['arrival']
            cur['wait'] = cur['tat'] - cur['burst_orig']
    return schedule, procs


def priority_nonpreemptive_algo(processes):
    procs = [{**p, 'burst_orig': p['burst']} for p in processes]
    time = 0
    schedule = []
    completed = 0
    n = len(procs)
    while completed < n:
        ready = [p for p in procs if p['arrival'] <= time and not p.get('done')]
        if not ready:
            time += 1
            continue
        ready.sort(key=lambda x: (x['priority'], x['arrival'], x['pid']))
        cur = ready[0]
        start = time
        time += cur['burst']
        cur['done'] = True
        cur['wait'] = start - cur['arrival']
        cur['tat'] = time - cur['arrival']
        schedule.append((start, cur['pid'], time))
        completed += 1
    return schedule, procs

# ------------------ GUI ------------------

class CPUSchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling Simulator - GUI")
        self.resizable(False, False)
        self.processes = []
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=0, column=0)

        # Input frame
        inp = ttk.LabelFrame(frm, text='Add Process')
        inp.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        ttk.Label(inp, text='Arrival:').grid(row=0, column=0)
        self.arrival_var = tk.StringVar(value='0')
        ttk.Entry(inp, width=6, textvariable=self.arrival_var).grid(row=0, column=1)

        ttk.Label(inp, text='Burst:').grid(row=0, column=2)
        self.burst_var = tk.StringVar(value='1')
        ttk.Entry(inp, width=6, textvariable=self.burst_var).grid(row=0, column=3)

        ttk.Label(inp, text='Priority:').grid(row=0, column=4)
        self.priority_var = tk.StringVar(value='0')
        ttk.Entry(inp, width=6, textvariable=self.priority_var).grid(row=0, column=5)

        ttk.Button(inp, text='Add', command=self.add_process).grid(row=0, column=6, padx=6)
        ttk.Button(inp, text='Clear All', command=self.clear_processes).grid(row=0, column=7)

        # Process list
        list_frame = ttk.LabelFrame(frm, text='Processes')
        list_frame.grid(row=1, column=0, sticky='nw', padx=5, pady=5)
        cols = ('PID', 'Arrival', 'Burst', 'Priority')
        self.tree = ttk.Treeview(list_frame, columns=cols, show='headings', height=6)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=70, anchor='center')
        self.tree.grid(row=0, column=0)

        # Controls
        ctrl = ttk.LabelFrame(frm, text='Controls')
        ctrl.grid(row=0, column=1, rowspan=2, padx=10, sticky='n')

        ttk.Label(ctrl, text='Algorithm:').grid(row=0, column=0, sticky='w')
        self.alg_var = tk.StringVar(value='FCFS')
        algs = ['FCFS', 'SJF (NP)', 'SRTF', 'Round Robin', 'Priority (NP)']
        ttk.Combobox(ctrl, values=algs, textvariable=self.alg_var, state='readonly', width=18).grid(row=1, column=0)

        ttk.Label(ctrl, text='Time Quantum (RR):').grid(row=2, column=0, sticky='w', pady=(8,0))
        self.quantum_var = tk.StringVar(value='2')
        ttk.Entry(ctrl, textvariable=self.quantum_var, width=6).grid(row=3, column=0)

        ttk.Button(ctrl, text='Run', command=self.run).grid(row=4, column=0, pady=8)
        ttk.Button(ctrl, text='Export Result', command=self.export_result).grid(row=5, column=0)

        # Output: metrics + Gantt
        out = ttk.LabelFrame(frm, text='Output')
        out.grid(row=2, column=0, columnspan=2, pady=8)

        self.txt = tk.Text(out, height=8, width=85)
        self.txt.grid(row=0, column=0, padx=6, pady=6)

        self.canvas = tk.Canvas(out, height=120, width=720, bg='white')
        self.canvas.grid(row=1, column=0, padx=6, pady=(0,6))

    def add_process(self):
        try:
            arrival = int(self.arrival_var.get())
            burst = int(self.burst_var.get())
            priority = int(self.priority_var.get())
            if arrival < 0 or burst <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Input error', 'Arrival must be >=0; Burst must be >0; Priority integer')
            return
        pid = len(self.processes) + 1
        p = {'pid': pid, 'arrival': arrival, 'burst': burst, 'priority': priority}
        self.processes.append(p)
        self.tree.insert('', 'end', values=(pid, arrival, burst, priority))
        # reset inputs
        self.burst_var.set('1')
        self.priority_var.set('0')

    def clear_processes(self):
        self.processes.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.txt.delete('1.0', tk.END)
        self.canvas.delete('all')

    def run(self):
        if not self.processes:
            messagebox.showwarning('No processes', 'Add at least one process')
            return
        alg = self.alg_var.get()
        procs_input = [dict(p) for p in self.processes]
        # make deep copy-like for safety
        if alg == 'FCFS':
            schedule, procs = fcfs_algo(procs_input)
        elif alg == 'SJF (NP)':
            schedule, procs = sjf_nonpreemptive_algo(procs_input)
        elif alg == 'SRTF':
            schedule, procs = srtf_algo(procs_input)
        elif alg == 'Round Robin':
            try:
                q = int(self.quantum_var.get())
            except ValueError:
                messagebox.showerror('Input error', 'Quantum must be integer')
                return
            schedule, procs = round_robin_algo(procs_input, q)
        elif alg == 'Priority (NP)':
            schedule, procs = priority_nonpreemptive_algo(procs_input)
        else:
            messagebox.showerror('Algorithm', 'Unknown algorithm')
            return
        self.show_result(schedule, procs)

    def show_result(self, schedule, procs):
        self.txt.delete('1.0', tk.END)
        # print Gantt text
        self.txt.insert(tk.END, 'Gantt (start -> PID -> end):\n')
        for s in schedule:
            self.txt.insert(tk.END, f'[{s[0]} -> P{s[1]} -> {s[2]}] ')
        self.txt.insert(tk.END, '\n\nPer-process (pid, arrival, burst, wait, tat):\n')
        waits = []
        tats = []
        for p in sorted(procs, key=lambda x: x['pid']):
            wait = p.get('wait', 0)
            tat = p.get('tat', 0)
            waits.append(wait)
            tats.append(tat)
            self.txt.insert(tk.END, f"P{p['pid']}: {p.get('arrival')} {p.get('burst_orig', p.get('burst'))} wait={wait} tat={tat}\n")
        self.txt.insert(tk.END, f"\nAverage waiting time = {avg(waits):.2f}\n")
        self.txt.insert(tk.END, f"Average turnaround time = {avg(tats):.2f}\n")
        # draw gantt
        self.draw_gantt(schedule)
        # store last result for export
        self.last_result = {'schedule': schedule, 'procs': procs}

    def draw_gantt(self, schedule):
        self.canvas.delete('all')
        if not schedule:
            return
        # Determine scale: map time range to width
        start_time = min(s[0] for s in schedule)
        end_time = max(s[2] for s in schedule)
        total = max(1, end_time - start_time)
        width = int(self.canvas.winfo_width()) - 20
        x0 = 10
        y0 = 20
        h = 40
        scale = width / total
        colors = ['#FFB6C1', '#ADD8E6', '#90EE90', '#FFD700', '#FFA07A', '#DDA0DD']
        pid_to_color = {}
        color_i = 0
        for seg in schedule:
            s, pid, e = seg
            if pid not in pid_to_color:
                pid_to_color[pid] = colors[color_i % len(colors)]; color_i += 1
            x_start = x0 + int((s - start_time) * scale)
            x_end = x0 + int((e - start_time) * scale)
            if x_end==x_start:
                x_end += 2
            self.canvas.create_rectangle(x_start, y0, x_end, y0+h, outline='black', fill=pid_to_color[pid])
            self.canvas.create_text((x_start+x_end)//2, y0 + h//2, text=f'P{pid}')
            # times
            self.canvas.create_text(x_start, y0+h+10, text=str(s), anchor='n')
        # final time
        self.canvas.create_text(x0 + int((end_time-start_time)*scale), y0+h+10, text=str(end_time), anchor='n')

    def export_result(self):
        if not hasattr(self, 'last_result'):
            messagebox.showwarning('No result', 'Run a schedule first')
            return
        f = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text', '*.txt')])
        if not f:
            return
        with open(f, 'w') as fh:
            schedule = self.last_result['schedule']
            procs = self.last_result['procs']
            fh.write('Gantt (start -> PID -> end):\n')
            for s in schedule:
                fh.write(f'[{s[0]} -> P{s[1]} -> {s[2]}] ')
            fh.write('\n\nPer-process (pid, arrival, burst, wait, tat):\n')
            for p in sorted(procs, key=lambda x: x['pid']):
                fh.write(f"P{p['pid']}: {p.get('arrival')} {p.get('burst_orig', p.get('burst'))} wait={p.get('wait',0)} tat={p.get('tat',0)}\n")
        messagebox.showinfo('Export', f'Result saved to {f}')


if __name__ == '__main__':
    app = CPUSchedulerGUI()
    app.mainloop()
