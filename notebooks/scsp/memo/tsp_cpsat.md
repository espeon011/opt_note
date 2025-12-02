In [ ]:
```python
from dataclasses import dataclass
from ortools.sat.python import cp_model
import opt_note.scsp as scsp
```

In [ ]:
```python
import marimo as mo
import nbformat
```

# 順序制約付き巡回セールスマン問題として定式化する

In [ ]:
```python
@dataclass
class Model:
    instance: list[str]
    solution: str | None = None
    best_bound: float = 0.0

    def solve(
        self, time_limit: int | None = 60, log: bool = False, *args, **kwargs
    ) -> str | None:
        cpmodel = cp_model.CpModel()
        cpsolver = cp_model.CpSolver()

        nodes = [
            (sidx, cidx)
            for sidx, s in enumerate(self.instance)
            for cidx, _ in enumerate(s)
        ]
        order = [cpmodel.new_int_var(1, len(nodes), "") for _ in nodes]

        dummy_idx = len(nodes)
        order.append(cpmodel.new_constant(0))

        arcs = []
        costs = dict()

        for nidx, (sidx, cidx) in enumerate(nodes):
            if cidx == 0:
                arcs.append((dummy_idx, nidx, cpmodel.new_bool_var("")))
                costs[(dummy_idx, nidx)] = 1
            if cidx == len(self.instance[sidx]) - 1:
                arcs.append((nidx, dummy_idx, cpmodel.new_bool_var("")))
                costs[(nidx, dummy_idx)] = 0

        for nidx1, (sidx1, cidx1) in enumerate(nodes):
            for nidx2, (sidx2, cidx2) in enumerate(nodes):
                if sidx1 == sidx2 and cidx1 + 1 != cidx2:
                    continue
                s1 = self.instance[sidx1]
                s2 = self.instance[sidx2]
                arcs.append((nidx1, nidx2, cpmodel.new_bool_var("")))
                costs[(nidx1, nidx2)] = (
                    0 if sidx1 < sidx2 and s1[cidx1] == s2[cidx2] else 1
                )

        cpmodel.add_circuit(arcs)

        for nidx1, nidx2, v in arcs:
            if nidx2 == dummy_idx:
                continue
            cpmodel.add(order[nidx2] == order[nidx1] + 1).only_enforce_if(v)

        nidx = -1
        for s in self.instance:
            for cidx, _ in enumerate(s):
                nidx += 1
                if cidx == 0:
                    continue
                cpmodel.add(order[nidx - 1] < order[nidx])

        cpmodel.minimize(sum(costs[(nidx1, nidx2)] * v for (nidx1, nidx2, v) in arcs))

        cpsolver.parameters.log_search_progress = log
        if time_limit is not None:
            cpsolver.parameters.max_time_in_seconds = time_limit
        status = cpsolver.solve(cpmodel)

        self.best_bound = cpsolver.best_objective_bound

        if status in {
            cp_model.cp_model_pb2.OPTIMAL,
            cp_model.cp_model_pb2.FEASIBLE,
        }:
            solution = ""
            current_node = dummy_idx
            current_char: str | None = None
            current_sidxs: set[int] = set()
            complete = False
            while True:
                for nidx1, nidx2, v in arcs:
                    if nidx1 == current_node and cpsolver.boolean_value(v):
                        if nidx2 == dummy_idx:
                            complete = True
                            break
                        sidx, cidx = nodes[nidx2]

                        if self.instance[sidx][cidx] != current_char or sidx in current_sidxs:
                            solution += self.instance[sidx][cidx]
                            current_sidxs.clear()

                        current_node = nidx2
                        current_char = self.instance[sidx][cidx]
                        current_sidxs.add(sidx)
                if complete:
                    break
            self.solution = solution
        else:
            self.solution = None

        return self.solution
```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n004k015-025.txt", log=True)
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 60 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x99bbd015ce8d5085)
> #Variables: 5'433 (#bools: 5'241 in objective) (5'433 primary variables)
>   - 5'348 Booleans in [0,1]
>   - 84 in [1,84]
>   - 1 constants in {0} 
> #kCircuit: 1
> #kLinear2: 5'424 (#enforced: 5'344)
> 
> Starting presolve at 0.00s
>   1.15e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.01e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=25 #num_dual_strengthening=1 
>   2.02e-05s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.91e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   8.01e-04s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 16'373 nodes and 32'315 arcs.
> [Symmetry] Symmetry computation done. time: 0.00102516 dtime: 0.00246339
>   9.38e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.59e-01s  1.63e-01d  [Probe] #probed=10'704 #new_binary_clauses=3'934 
>   2.39e-05s  0.00e+00d  [MaxClique] 
>   1.16e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.52e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   5.91e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   8.08e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.00e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.23e-05s  4.80e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=80 
>   1.45e-03s  0.00e+00d  [DetectDifferentVariables] #different=80 
>   2.31e-05s  0.00e+00d  [ProcessSetPPC] 
>   3.12e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   3.12e-04s  1.05e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   8.01e-04s  5.10e-04d  [FindBigVerticalLinearOverlap] 
>   1.99e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.70e-05s  0.00e+00d  [MergeClauses] 
>   1.30e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.23e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.30e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.20e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.99e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.04e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 26'893 nodes and 48'095 arcs.
> [Symmetry] Symmetry computation done. time: 0.00330301 dtime: 0.0081293
> [SAT presolve] num removable Booleans: 0 / 5348
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:2630 literals:5260 vars:5260 one_side_vars:5260 simple_definition:0 singleton_clauses:0
> [SAT presolve] [8.6504e-05s] clauses:2630 literals:5260 vars:5260 one_side_vars:5260 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000134656s] clauses:2630 literals:5260 vars:5260 one_side_vars:5260 simple_definition:0 singleton_clauses:0
>   9.94e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.61e-01s  1.63e-01d  [Probe] #probed=10'704 #new_binary_clauses=1'304 
>   4.54e-03s  1.35e-02d  [MaxClique] Merged 2'630(5'260 literals) into 2'626(5'260 literals) at_most_ones. 
>   1.32e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.27e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.34e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   8.83e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.45e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.47e-05s  4.80e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=80 
>   1.14e-03s  0.00e+00d  [DetectDifferentVariables] #different=80 
>   4.28e-04s  1.58e-05d  [ProcessSetPPC] #relevant_constraints=2'626 
>   4.57e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.59e-04s  6.31e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   8.28e-04s  5.37e-04d  [FindBigVerticalLinearOverlap] 
>   3.44e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   3.70e-05s  0.00e+00d  [MergeClauses] 
>   1.49e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.26e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.49e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.24e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.20e-04s  0.00e+00d  [DetectDuplicateColumns] 
>   1.24e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=2'622 
> [Symmetry] Graph for symmetry has 26'897 nodes and 48'111 arcs.
> [Symmetry] Symmetry computation done. time: 0.0033265 dtime: 0.00813111
> [SAT presolve] num removable Booleans: 0 / 5348
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:2630 literals:5260 vars:5260 one_side_vars:5260 simple_definition:0 singleton_clauses:0
> [SAT presolve] [8.4761e-05s] clauses:2630 literals:5260 vars:5260 one_side_vars:5260 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000133293s] clauses:2630 literals:5260 vars:5260 one_side_vars:5260 simple_definition:0 singleton_clauses:0
>   1.14e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   4.49e-01s  1.63e-01d  [Probe] #probed=10'704 #new_binary_clauses=1'288 
>   4.60e-03s  1.35e-02d  [MaxClique] Merged 2'634(5'276 literals) into 2'626(5'260 literals) at_most_ones. 
>   1.38e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.31e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.94e-04s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   9.16e-04s  0.00e+00d  [DetectDuplicateConstraints] 
>   8.64e-04s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   6.68e-05s  4.80e-07d  [DetectDominatedLinearConstraints] #relevant_constraints=80 
>   1.23e-03s  0.00e+00d  [DetectDifferentVariables] #different=80 
>   4.53e-04s  1.58e-05d  [ProcessSetPPC] #relevant_constraints=2'626 
>   6.60e-05s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   6.64e-04s  6.31e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   8.34e-04s  5.37e-04d  [FindBigVerticalLinearOverlap] 
>   5.46e-05s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   5.61e-05s  0.00e+00d  [MergeClauses] 
>   1.53e-03s  0.00e+00d  [DetectDominanceRelations] 
>   1.31e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.28e-04s  0.00e+00d  [ExpandObjective] 
> 
> Presolve summary:
>   - 0 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 48'168 times.
>   - rule 'at_most_one: transformed into max clique.' was applied 2 times.
>   - rule 'deductions: 10001 stored' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 2'622 times.
>   - rule 'incompatible linear: add implication' was applied 7'890 times.
>   - rule 'linear: reduced variable domains' was applied 856 times.
>   - rule 'presolve: 1 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: detect half reified value encoding' was applied 4 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xb721ce293dbb1f8f)
> #Variables: 5'432 (#bools: 5'241 in objective) (5'432 primary variables)
>   - 5'348 Booleans in [0,1]
>   - 1 in [1,60]
>   - 2 in [1,64]
>   - 1 in [1,68]
>   - 1 in [2,61]
>   - 2 in [2,65]
>   - 1 in [2,69]
>   - 1 in [3,62]
>   - 2 in [3,66]
>   - 1 in [3,70]
>   - 1 in [4,63]
>   - 2 in [4,67]
>   - 1 in [4,71]
>   - 1 in [5,64]
>   - 2 in [5,68]
>   - 1 in [5,72]
>   - 1 in [6,65]
>   - 2 in [6,69]
>   - 1 in [6,73]
>   - 1 in [7,66]
>   - 2 in [7,70]
>   - 1 in [7,74]
>   - 1 in [8,67]
>   - 2 in [8,71]
>   - 1 in [8,75]
>   - 1 in [9,68]
>   - 2 in [9,72]
>   - 1 in [9,76]
>   - 1 in [10,69]
>   - 2 in [10,73]
>   - 1 in [10,77]
>   - 1 in [11,70]
>   - 2 in [11,74]
>   - 1 in [11,78]
>   - 1 in [12,71]
>   - 2 in [12,75]
>   - 1 in [12,79]
>   - 1 in [13,72]
>   - 2 in [13,76]
>   - 1 in [13,80]
>   - 1 in [14,73]
>   - 2 in [14,77]
>   - 1 in [14,81]
>   - 1 in [15,74]
>   - 2 in [15,78]
>   - 1 in [15,82]
>   - 1 in [16,75]
>   - 2 in [16,79]
>   - 1 in [16,83]
>   - 1 in [17,76]
>   - 2 in [17,80]
>   - 1 in [17,84]
>   - 1 in [18,77]
>   - 2 in [18,81]
>   - 1 in [19,78]
>   - 2 in [19,82]
>   - 1 in [20,79]
>   - 2 in [20,83]
>   - 1 in [21,80]
>   - 2 in [21,84]
>   - 1 in [22,81]
>   - 1 in [23,82]
>   - 1 in [24,83]
>   - 1 in [25,84]
> #kAtMostOne: 4 (#literals: 16)
> #kBoolAnd: 5'252 (#enforced: 5'252) (#literals: 10'504)
> #kCircuit: 1
> #kLinear1: 4 (#enforced: 4)
> #kLinear2: 5'420 (#enforced: 5'340)
> [Symmetry] Graph for symmetry has 26'896 nodes and 48'111 arcs.
> [Symmetry] Symmetry computation done. time: 0.003126 dtime: 0.00813105
> 
> Preloading model.
> #Bound   1.64s best:inf   next:[0,5241]   initial_domain
> #Model   1.65s var:5432/5432 constraints:10681/10681
> 
> Starting search at 1.65s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 12 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns, routing_path_lns, routing_random_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #Bound   2.79s best:inf   next:[50,5241]  fs_random
> #1       2.82s best:83    next:[50,82]    fs_random_no_lp
> #2       3.33s best:82    next:[50,81]    graph_cst_lns (d=5.00e-01 s=88 t=0.10 p=0.00 stall=0 h=base)
> #3       3.36s best:81    next:[50,80]    graph_arc_lns (d=5.00e-01 s=87 t=0.10 p=0.00 stall=0 h=base)
> #4       3.99s best:79    next:[50,78]    rnd_cst_lns (d=7.07e-01 s=95 t=0.10 p=1.00 stall=1 h=base)
> #5       4.25s best:78    next:[50,77]    graph_dec_lns (d=7.07e-01 s=97 t=0.10 p=1.00 stall=1 h=base)
> #6       5.11s best:77    next:[50,76]    graph_dec_lns (d=6.92e-01 s=130 t=0.10 p=0.67 stall=1 h=base)
> #7       5.63s best:76    next:[50,75]    quick_restart
> #Bound   5.90s best:76    next:[51,75]    reduced_costs
> #8       6.27s best:75    next:[51,74]    graph_dec_lns (d=5.54e-01 s=159 t=0.10 p=0.50 stall=0 h=base)
> #9       6.41s best:74    next:[51,73]    graph_cst_lns (d=6.31e-01 s=157 t=0.10 p=0.60 stall=1 h=base)
> #10      6.67s best:73    next:[51,72]    graph_var_lns (d=9.91e-01 s=169 t=0.10 p=0.93 stall=14 h=stalling)
> #11      7.11s best:72    next:[51,71]    graph_var_lns (d=9.94e-01 s=172 t=0.10 p=0.94 stall=0 h=base)
> #12      7.50s best:71    next:[51,70]    graph_dec_lns (d=6.62e-01 s=182 t=0.10 p=0.57 stall=2 h=base) [combined with: graph_var_lns (d=9.9...]
> #13      9.35s best:70    next:[51,69]    rnd_var_lns (d=7.22e-01 s=210 t=0.10 p=0.55 stall=1 h=base)
> #Bound  12.33s best:70    next:[52,69]    reduced_costs
> #14     22.68s best:69    next:[52,68]    quick_restart
> #15     25.00s best:68    next:[52,67]    routing_path_lns (d=2.92e-01 s=552 t=0.10 p=0.44 stall=0 h=routing)
> #Bound  30.68s best:68    next:[53,67]    max_lp
> #Bound  30.83s best:68    next:[54,67]    max_lp
> #16     36.44s best:67    next:[54,66]    quick_restart
> #17     37.03s best:66    next:[54,65]    graph_cst_lns (d=5.60e-01 s=847 t=0.10 p=0.50 stall=18 h=stalling)
> #Bound  37.51s best:66    next:[55,65]    max_lp
> #Bound  37.66s best:66    next:[56,65]    max_lp
> #18     43.70s best:65    next:[56,64]    quick_restart
> #19     58.51s best:64    next:[56,63]    default_lp
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [  58.37s,   58.37s]   58.37s   0.00ns   58.37s         1 [   8.31s,    8.31s]    8.31s   0.00ns    8.31s
>            'default_lp':         1 [  58.35s,   58.35s]   58.35s   0.00ns   58.35s         1 [  16.04s,   16.04s]   16.04s   0.00ns   16.04s
>      'feasibility_pump':       217 [190.65us,  23.04ms] 919.66us   1.84ms 199.57ms       210 [156.29us,   9.05ms] 198.62us 612.02us  41.71ms
>                    'fj':        18 [  6.23ms, 139.94ms]  62.64ms  61.99ms    1.13s        18 [100.02ms, 118.63ms] 103.50ms   4.95ms    1.86s
>                    'fj':        19 [  6.06ms, 145.54ms]  66.29ms  62.78ms    1.26s        19 [100.02ms, 107.56ms] 101.99ms   2.43ms    1.94s
>             'fs_random':         1 [   1.17s,    1.17s]    1.17s   0.00ns    1.17s         1 [  5.70ms,   5.70ms]   5.70ms   0.00ns   5.70ms
>       'fs_random_no_lp':         1 [   1.18s,    1.18s]    1.18s   0.00ns    1.18s         1 [  1.75ms,   1.75ms]   1.75ms   0.00ns   1.75ms
>         'graph_arc_lns':        59 [ 20.87ms, 797.68ms] 378.26ms 243.32ms   22.32s        59 [ 20.00ns, 100.31ms]  60.64ms  43.93ms    3.58s
>         'graph_cst_lns':        64 [ 11.89ms,    1.00s] 351.87ms 295.83ms   22.52s        64 [ 10.00ns, 100.36ms]  53.40ms  47.38ms    3.42s
>         'graph_dec_lns':        76 [ 12.54ms, 792.01ms] 296.14ms 242.67ms   22.51s        76 [ 10.00ns, 100.17ms]  53.86ms  47.77ms    4.09s
>         'graph_var_lns':       111 [ 16.71ms, 452.89ms] 199.62ms 129.83ms   22.16s       111 [ 10.00ns, 102.33ms]  51.63ms  46.34ms    5.73s
>                    'ls':       217 [  7.40ms, 148.43ms]  51.92ms  53.13ms   11.27s       217 [100.02ms, 110.82ms] 103.13ms   3.91ms   22.38s
>                'ls_lin':       214 [  7.31ms, 139.36ms]  65.56ms  53.88ms   14.03s       214 [ 93.23ms, 110.68ms] 102.27ms   3.65ms   21.89s
>                'max_lp':         1 [  58.35s,   58.35s]   58.35s   0.00ns   58.35s         1 [  19.40s,   19.40s]   19.40s   0.00ns   19.40s
>                 'no_lp':         1 [  58.37s,   58.37s]   58.37s   0.00ns   58.37s         1 [  10.87s,   10.87s]   10.87s   0.00ns   10.87s
>          'pseudo_costs':         1 [  58.34s,   58.34s]   58.34s   0.00ns   58.34s         1 [  17.38s,   17.38s]   17.38s   0.00ns   17.38s
>         'quick_restart':         1 [  58.38s,   58.38s]   58.38s   0.00ns   58.38s         1 [  15.55s,   15.55s]   15.55s   0.00ns   15.55s
>   'quick_restart_no_lp':         1 [  58.35s,   58.35s]   58.35s   0.00ns   58.35s         1 [   9.00s,    9.00s]    9.00s   0.00ns    9.00s
>         'reduced_costs':         1 [  58.37s,   58.37s]   58.37s   0.00ns   58.37s         1 [  21.85s,   21.85s]   21.85s   0.00ns   21.85s
>             'rins/rens':        72 [  1.38ms,    1.15s] 335.96ms 382.70ms   24.19s        46 [ 10.00ns, 101.75ms]  61.61ms  44.80ms    2.83s
>           'rnd_cst_lns':        69 [ 18.22ms, 788.07ms] 326.86ms 247.53ms   22.55s        69 [ 10.00ns, 100.23ms]  53.54ms  46.89ms    3.69s
>           'rnd_var_lns':       102 [ 17.95ms, 494.54ms] 216.38ms 140.53ms   22.07s        98 [  5.53us, 100.19ms]  55.77ms  44.97ms    5.47s
>      'routing_path_lns':        50 [ 87.28ms, 989.43ms] 454.85ms 248.27ms   22.74s        50 [  1.79ms, 100.35ms]  64.88ms  39.62ms    3.24s
>    'routing_random_lns':        42 [ 68.82ms,    1.05s] 527.58ms 242.06ms   22.16s        42 [129.99us, 100.31ms]  71.48ms  37.63ms    3.00s
> 
> Search stats              Bools  Conflicts   Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  5'352     27'960    559'766    47'153  22'339'379     28'261'744
>            'default_lp':  5'352      4'120    414'794    71'166  13'924'137     21'619'972
>             'fs_random':  5'352          1     10'725    10'704     679'898        838'024
>       'fs_random_no_lp':  5'352          0     10'768    10'705     683'578        829'798
>                'max_lp':  5'393      1'205    234'236    45'640   5'828'863      9'893'984
>                 'no_lp':  5'352     58'351    372'901    34'475  11'166'162     27'238'899
>          'pseudo_costs':  5'424      1'177    157'493    34'024   4'176'771      7'108'386
>         'quick_restart':  5'390      3'423    613'709    66'001  11'074'393     19'283'166
>   'quick_restart_no_lp':  5'415     16'797  1'651'182    41'874  18'702'093     34'938'728
>         'reduced_costs':  5'352      1'029    237'378    39'828   4'803'265      7'994'441
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':        22'325   5'687'857   2'044'245     1'101'071        58     7'865     120'268         0      1'205        5'648      843
>            'default_lp':         1'154      62'751      71'117             0        17    13'530     210'730         0        496        2'747    2'434
>             'fs_random':             0           0           2             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':           802      75'494      60'601             0        12     2'394     126'990         0         41          158       94
>                 'no_lp':        51'137  19'549'010  13'317'510     9'443'760       458     2'200      85'659         0         95          346      289
>          'pseudo_costs':           786      90'623      98'395             0         5     1'632      84'760         0         36          148       62
>         'quick_restart':         1'483     105'623     236'075             0        17     6'488     205'439         0        345        3'321      797
>   'quick_restart_no_lp':         8'456   1'307'073   1'872'068             0        38     8'981     113'075         0      1'550       15'120    1'141
>         'reduced_costs':           209       3'930      17'242             0         0     2'030     105'913         0         83          300      112
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          5     257'675          0   31'572       44        0
>       'fs_random':          5         957          0       46        0        0
>          'max_lp':          1     146'581      7'755    3'946    1'867       17
>    'pseudo_costs':          1     144'447      8'361    5'138    1'029        1
>   'quick_restart':          5     258'717          0   36'674       20        1
>   'reduced_costs':          1     189'852      6'664    4'452      654        0
> 
> Lp dimension            Final dimension of first component
>      'default_lp':   169 rows, 5348 columns, 10632 entries
>       'fs_random':   170 rows, 5348 columns, 10696 entries
>          'max_lp':  1554 rows, 5432 columns, 30458 entries
>    'pseudo_costs':   937 rows, 5432 columns, 26870 entries
>   'quick_restart':   169 rows, 5348 columns, 10632 entries
>   'reduced_costs':   923 rows, 5432 columns, 17820 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0   5'827         0  15'215           0
>    'pseudo_costs':          0            0   6'141         0   9'812           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0   5'097         0  12'058           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened     Cuts/Call
>      'default_lp':          254        0        0     170          0      0             0           0/0
>       'fs_random':          254        0        0     170          0      0             0           0/0
>          'max_lp':       21'315      237        0     170          0     12         1'579  7'755/12'092
>    'pseudo_costs':       21'920      143      194     171          0      5         1'256  8'361/13'268
>   'quick_restart':          254        0        0     170          0      0             0           0/0
>   'reduced_costs':       20'224      199        0     170          0     15         1'405  6'664/11'162
> 
> Lp Cut             max_lp  pseudo_costs  reduced_costs
>            CG_FF:      41            38             49
>             CG_K:       9            21             22
>             CG_R:      43            24             26
>            CG_RB:      35            51             50
>           CG_RBP:      26            14             11
>          Circuit:     525           583            486
>   CircuitBlossom:       2             4              1
>     CircuitExact:      13             6              1
>           Clique:      52            52             41
>               IB:   5'993         6'970          5'142
>         MIR_1_FF:      94            61             71
>          MIR_1_K:      15             4              3
>         MIR_1_KL:       1             1              -
>          MIR_1_R:       1             -              -
>         MIR_1_RB:      94            70            112
>        MIR_1_RBP:      12             7             27
>         MIR_2_FF:      35            41             35
>          MIR_2_K:       6             1              -
>         MIR_2_KL:       1             -              -
>          MIR_2_R:       2             4              5
>         MIR_2_RB:      58            41             68
>        MIR_2_RBP:       9             7             12
>         MIR_3_FF:      29            33             22
>          MIR_3_K:       5             1              1
>         MIR_3_KL:       2             -              -
>          MIR_3_R:       2             7              7
>         MIR_3_RB:      43            30             40
>        MIR_3_RBP:       4             4              6
>         MIR_4_FF:      15            22             22
>          MIR_4_K:       4             -              1
>         MIR_4_KL:       1             1              -
>          MIR_4_R:       -             6              4
>         MIR_4_RB:      34            25             30
>        MIR_4_RBP:       2             4              7
>         MIR_5_FF:      20            13             12
>          MIR_5_K:       2             -              2
>          MIR_5_R:       2             2              5
>         MIR_5_RB:      26            22             22
>        MIR_5_RBP:       2             1              5
>         MIR_6_FF:      20            15             11
>          MIR_6_K:       3             2              1
>         MIR_6_KL:       1             -              -
>          MIR_6_R:       -             3              4
>         MIR_6_RB:      22            15             22
>        MIR_6_RBP:       2             -              4
>     ZERO_HALF_FF:      51             6              8
>      ZERO_HALF_K:      12             -              -
>     ZERO_HALF_KL:       1             -              -
>      ZERO_HALF_R:     331           112            199
>     ZERO_HALF_RB:      43            30             59
>    ZERO_HALF_RBP:       9             7              8
> 
> LNS stats                Improv/Calls  Closed  Difficulty  TimeLimit
>        'graph_arc_lns':          5/59     47%    3.85e-01       0.10
>        'graph_cst_lns':          8/64     52%    6.74e-01       0.10
>        'graph_dec_lns':          6/76     50%    5.64e-01       0.10
>        'graph_var_lns':         2/111     56%    9.92e-01       0.10
>            'rins/rens':         30/47     47%    1.84e-01       0.10
>          'rnd_cst_lns':          4/69     51%    6.19e-01       0.10
>          'rnd_var_lns':          6/98     50%    7.18e-01       0.10
>     'routing_path_lns':         12/50     50%    4.41e-01       0.10
>   'routing_random_lns':          7/42     52%    5.99e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        1                  1     1'285         0              0          0             69        293'468
>                     'fj_restart_compound':        6                  2         0       225            198          0              0         11'706
>                 'fj_restart_compound_obj':        1                  1         0        52             47          0              0          1'879
>             'fj_restart_compound_perturb':        5                  4         0       156            148          0              0         10'084
>         'fj_restart_compound_perturb_obj':        1                  1         0        34             31          0              0          1'953
>                        'fj_restart_decay':        8                  3    11'932         0              0          0            226      1'749'399
>               'fj_restart_decay_compound':        2                  2         0       101             74          0              0          3'888
>   'fj_restart_decay_compound_perturb_obj':        5                  5         0       176            163          0              0          9'935
>                'fj_restart_decay_perturb':        1                  1     1'399         0              0          0             29        292'566
>            'fj_restart_decay_perturb_obj':        1                  1     1'364         0              0          0             30        299'106
>                          'fj_restart_obj':        6                  3     7'653         0              0          0            375      1'822'201
>                          'ls_lin_restart':       21                 18    15'961         0              0          0          5'514      1'842'188
>                 'ls_lin_restart_compound':       11                  9         0       213              0        106              0         20'992
>         'ls_lin_restart_compound_perturb':       22                 18         0       424              0        211              0         42'021
>                    'ls_lin_restart_decay':       37                 26    31'460         0              0          0          1'426      6'101'968
>           'ls_lin_restart_decay_compound':       34                 24         0       643              1        318              0         63'860
>   'ls_lin_restart_decay_compound_perturb':       33                 24         0       635              0        315              0         62'824
>            'ls_lin_restart_decay_perturb':       24                 21    20'584         0              0          0          1'105      4'051'101
>                  'ls_lin_restart_perturb':       32                 24    22'837         0              0          0          8'085      2'748'594
>                              'ls_restart':       17                 13    12'011         0              0          0          5'148      1'169'217
>                     'ls_restart_compound':       16                 14         0       306              0        151              0         30'127
>             'ls_restart_compound_perturb':       42                 27         0       812              1        404              0         80'475
>                        'ls_restart_decay':       24                 22    20'895         0              0          0          1'135      4'096'837
>               'ls_restart_decay_compound':       30                 20         0       583              0        290              0         57'494
>       'ls_restart_decay_compound_perturb':       41                 30         0       778              0        387              0         77'553
>                'ls_restart_decay_perturb':       19                 18    16'451         0              0          0            916      3'213'122
>                      'ls_restart_perturb':       28                 24    19'783         0              0          0          7'835      2'172'422
> 
> Solutions (19)         Num     Rank
>         'default_lp':    1  [19,19]
>    'fs_random_no_lp':    1    [1,1]
>      'graph_arc_lns':    1    [3,3]
>      'graph_cst_lns':    3   [2,17]
>      'graph_dec_lns':    4   [5,12]
>      'graph_var_lns':    2  [10,11]
>      'quick_restart':    4   [7,18]
>        'rnd_cst_lns':    1    [4,4]
>        'rnd_var_lns':    1  [13,13]
>   'routing_path_lns':    1  [15,15]
> 
> Objective bounds     Num
>        'fs_random':    1
>   'initial_domain':    1
>           'max_lp':    4
>    'reduced_costs':    2
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':    176    1'622      123
>    'fj solution hints':     16        0       16
>         'lp solutions':  1'181       26      609
>                 'pump':    216       46
> 
> Improving bounds shared    Num  Sym
>          'quick_restart':    3    0
> 
> Clauses shared              Num
>                  'core':  1'998
>            'default_lp':    906
>             'fs_random':      1
>                'max_lp':    119
>                 'no_lp':  1'434
>          'pseudo_costs':    144
>         'quick_restart':    982
>   'quick_restart_no_lp':  4'178
>         'reduced_costs':    487
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 64
> best_bound: 56
> integers: 5505
> booleans: 5352
> conflicts: 1
> branches: 10725
> propagations: 679898
> integer_propagations: 838024
> restarts: 10704
> lp_iterations: 957
> walltime: 60.0334
> usertime: 60.0334
> deterministic_time: 202.103
> gap_integral: 485.632
> solution_fingerprint: 0x16315e395d3a2d9c
> 
> --- Condition (with 25 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> 
> --- Solution (of length 64) ---
>  Sol: tkiojgnekulcinqyfcosohvmaozpxplngbrdxdhbxctsvsruqpvnngxzvxissbxf
> str1: tk---gn-ku-----------h-m---px--n------h---t-----q----gxzvxis----
> str2: --ioj-------i-q-f-o-----------ln-b--x---xc--vs-uqpv-------issbxf
> str3: ---------ulcin-y-coso-v--ozp-pl------------------p--------------
> str4: --i--g-e--------------v-a-z-----gbrd-d-b-c-sv-r---vnng---------f
> 
> example file name: 'uniform_q26n004k015-025.txt'
> best objective: 64
> best bound: 56.0
> wall time: 60.215703s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n008k015-025.txt", log=True)
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 60 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x6d8144a6890fd4cf)
> #Variables: 27'109 (#bools: 26'353 in objective) (27'109 primary variables)
>   - 26'933 Booleans in [0,1]
>   - 175 in [1,175]
>   - 1 constants in {0} 
> #kCircuit: 1
> #kLinear2: 27'092 (#enforced: 26'925)
> 
> Starting presolve at 0.01s
>   5.78e-03s  0.00e+00d  [DetectDominanceRelations] 
>   5.27e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=25 #num_dual_strengthening=1 
>   1.33e-04s  0.00e+00d  [ExtractEncodingFromLinear] 
>   1.21e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   4.69e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 81'484 nodes and 162'074 arcs.
> [Symmetry] Symmetry computation done. time: 0.0051507 dtime: 0.0123967
>   5.32e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.04e+00s  1.00e+00d *[Probe] #probed=28'888 #new_binary_clauses=13'332 
>   1.07e-04s  0.00e+00d  [MaxClique] 
>   5.81e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.62e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   2.96e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   4.65e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   4.49e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.32e-04s  1.00e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=167 
>   8.42e-03s  0.00e+00d  [DetectDifferentVariables] #different=167 
>   2.39e-04s  0.00e+00d  [ProcessSetPPC] 
>   3.04e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.99e-03s  5.32e-04d  [FindBigAtMostOneAndLinearOverlap] 
>   5.81e-03s  2.56e-03d  [FindBigVerticalLinearOverlap] 
>   1.07e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   9.64e-05s  0.00e+00d  [MergeClauses] 
>   6.88e-03s  0.00e+00d  [DetectDominanceRelations] 
>   6.41e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.80e-03s  0.00e+00d  [DetectDominanceRelations] 
>   6.38e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.24e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   4.96e-03s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 134'984 nodes and 242'324 arcs.
> [Symmetry] Symmetry computation done. time: 0.0189432 dtime: 0.0415452
> [SAT presolve] num removable Booleans: 0 / 26933
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:13375 literals:26750 vars:26750 one_side_vars:26750 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000409818s] clauses:13375 literals:26750 vars:26750 one_side_vars:26750 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000640696s] clauses:13375 literals:26750 vars:26750 one_side_vars:26750 simple_definition:0 singleton_clauses:0
>   5.45e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.03e+00s  1.00e+00d *[Probe] #probed=28'886 #new_binary_clauses=2'464 
>   4.87e-02s  1.65e-01d  [MaxClique] 
>   7.26e-03s  0.00e+00d  [DetectDominanceRelations] 
>   6.89e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.59e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   5.98e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   5.31e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.84e-04s  1.00e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=167 
>   8.41e-03s  0.00e+00d  [DetectDifferentVariables] #different=167 
>   2.94e-03s  8.02e-05d  [ProcessSetPPC] #relevant_constraints=13'375 
>   6.78e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   5.67e-03s  3.20e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   6.82e-03s  2.70e-03d  [FindBigVerticalLinearOverlap] 
>   2.88e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   3.03e-04s  0.00e+00d  [MergeClauses] 
>   8.34e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.12e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   8.13e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.19e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.49e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   8.25e-03s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=13'375 
> [Symmetry] Graph for symmetry has 134'984 nodes and 242'324 arcs.
> [Symmetry] Symmetry computation done. time: 0.0192292 dtime: 0.0415452
> [SAT presolve] num removable Booleans: 0 / 26933
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:13375 literals:26750 vars:26750 one_side_vars:26750 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000424566s] clauses:13375 literals:26750 vars:26750 one_side_vars:26750 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.000663819s] clauses:13375 literals:26750 vars:26750 one_side_vars:26750 simple_definition:0 singleton_clauses:0
>   5.80e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.06e+00s  1.00e+00d *[Probe] #probed=28'886 #new_binary_clauses=2'464 
>   4.97e-02s  1.65e-01d  [MaxClique] 
>   7.66e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.05e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   6.82e-03s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   6.30e-03s  0.00e+00d  [DetectDuplicateConstraints] 
>   5.73e-03s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   7.03e-04s  1.00e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=167 
>   8.85e-03s  0.00e+00d  [DetectDifferentVariables] #different=167 
>   3.43e-03s  8.02e-05d  [ProcessSetPPC] #relevant_constraints=13'375 
>   9.61e-04s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   5.93e-03s  3.20e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   6.95e-03s  2.70e-03d  [FindBigVerticalLinearOverlap] 
>   5.99e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   6.34e-04s  0.00e+00d  [MergeClauses] 
>   8.88e-03s  0.00e+00d  [DetectDominanceRelations] 
>   7.31e-02s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.98e-03s  0.00e+00d  [ExpandObjective] 
> 
> Presolve summary:
>   - 0 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 242'469 times.
>   - rule 'deductions: 51323 stored' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 13'375 times.
>   - rule 'incompatible linear: add implication' was applied 40'125 times.
>   - rule 'linear: reduced variable domains' was applied 1'850 times.
>   - rule 'presolve: 1 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: detect half reified value encoding' was applied 8 times.
> 
> Presolved optimization model '': (model_fingerprint: 0xec2171d65916dbe3)
> #Variables: 27'108 (#bools: 26'353 in objective) (27'108 primary variables)
>   - 26'933 Booleans in [0,1]
>   - 108 different domains in [1,175] with a largest complexity of 1.
> #kBoolAnd: 26'750 (#enforced: 26'750) (#literals: 53'500)
> #kCircuit: 1
> #kLinear1: 8 (#enforced: 8)
> #kLinear2: 27'084 (#enforced: 26'917)
> [Symmetry] Graph for symmetry has 134'983 nodes and 242'324 arcs.
> [Symmetry] Symmetry computation done. time: 0.0182246 dtime: 0.0415451
> 
> Preloading model.
> #Bound  10.67s best:inf   next:[0,26353]  initial_domain
> #Model  10.68s var:27108/27108 constraints:53843/53843
> 
> Starting search at 10.68s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 12 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns, routing_path_lns, routing_random_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #Bound  19.61s best:inf   next:[61,26353] pseudo_costs
> #1      19.73s best:175   next:[61,174]   fs_random_no_lp
> #2      20.49s best:171   next:[61,170]   rnd_cst_lns (d=5.00e-01 s=415 t=0.10 p=0.00 stall=0 h=base)
> #3      23.34s best:170   next:[61,169]   graph_dec_lns (d=7.07e-01 s=442 t=0.10 p=1.00 stall=1 h=base)
> #4      25.56s best:169   next:[61,168]   rnd_cst_lns (d=4.46e-01 s=477 t=0.10 p=0.50 stall=3 h=base)
> #5      25.82s best:168   next:[61,167]   rnd_var_lns (d=5.97e-01 s=499 t=0.10 p=0.50 stall=4 h=base)
> #6      26.39s best:166   next:[61,165]   routing_path_lns (d=1.86e-01 s=503 t=0.10 p=0.00 stall=1 h=routing)
> #7      27.59s best:164   next:[61,163]   graph_var_lns (d=9.97e-01 s=514 t=0.10 p=1.00 stall=16 h=base)
> #8      28.96s best:163   next:[61,162]   rnd_var_lns (d=7.09e-01 s=535 t=0.10 p=0.57 stall=2 h=base)
> #9      29.10s best:161   next:[61,160]   graph_dec_lns (d=5.19e-01 s=538 t=0.10 p=0.50 stall=1 h=base)
> #10     30.10s best:160   next:[61,159]   routing_random_lns (d=1.92e-01 s=555 t=0.10 p=0.25 stall=1 h=routing)
> #11     31.42s best:159   next:[61,158]   graph_dec_lns (d=5.08e-01 s=569 t=0.10 p=0.50 stall=1 h=base)
> #12     33.77s best:158   next:[61,157]   graph_dec_lns (d=5.00e-01 s=602 t=0.10 p=0.50 stall=1 h=base)
> #13     34.67s best:157   next:[61,156]   rnd_var_lns (d=7.02e-01 s=605 t=0.10 p=0.55 stall=3 h=base)
> #14     35.21s best:156   next:[61,155]   graph_var_lns (d=9.96e-01 s=619 t=0.10 p=0.83 stall=3 h=base)
> #15     35.22s best:155   next:[61,154]   graph_var_lns (d=9.96e-01 s=619 t=0.10 p=0.83 stall=3 h=base) [combined with: rnd_var_lns (d=7.02e...]
> #16     36.60s best:153   next:[61,152]   graph_dec_lns (d=6.08e-01 s=634 t=0.10 p=0.55 stall=2 h=base)
> #17     37.56s best:152   next:[61,151]   graph_arc_lns (d=3.96e-01 s=637 t=0.10 p=0.50 stall=5 h=base)
> #18     39.85s best:151   next:[61,150]   graph_arc_lns (d=4.97e-01 s=677 t=0.10 p=0.54 stall=2 h=base)
> #19     40.14s best:150   next:[61,149]   ls_lin_restart_decay(batch:1 lin{mvs:78 evals:21'218} #w_updates:30 #perturb:0)
> #20     40.38s best:149   next:[61,148]   graph_arc_lns (d=4.97e-01 s=678 t=0.10 p=0.54 stall=2 h=base) [combined with: ls_lin_restart_decay...]
> #21     41.13s best:148   next:[61,147]   rnd_var_lns (d=6.88e-01 s=693 t=0.10 p=0.53 stall=2 h=base)
> #22     44.82s best:147   next:[61,146]   graph_cst_lns (d=4.26e-01 s=742 t=0.10 p=0.45 stall=11 h=base)
> #23     50.34s best:146   next:[61,145]   rnd_cst_lns (d=4.99e-01 s=805 t=0.10 p=0.52 stall=6 h=base)
> #24     52.58s best:145   next:[61,144]   graph_dec_lns (d=5.69e-01 s=820 t=0.10 p=0.53 stall=6 h=base)
> #Bound  58.52s best:145   next:[62,144]   pseudo_costs
> #25     59.51s best:144   next:[62,143]   routing_path_lns (d=1.69e-01 s=951 t=0.10 p=0.44 stall=10 h=stalling)
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [  49.39s,   49.39s]   49.39s   0.00ns   49.39s         1 [   3.91s,    3.91s]    3.91s   0.00ns    3.91s
>            'default_lp':         1 [  49.35s,   49.35s]   49.35s   0.00ns   49.35s         1 [   9.20s,    9.20s]    9.20s   0.00ns    9.20s
>      'feasibility_pump':       148 [867.29us, 154.12ms]   4.58ms  16.99ms 678.19ms       105 [703.85us,  81.19ms]   1.47ms   7.82ms 154.39ms
>                    'fj':        88 [  4.74ms, 226.63ms] 101.75ms  87.60ms    8.95s        88 [100.09ms, 170.89ms] 107.17ms  13.64ms    9.43s
>                    'fj':       105 [  4.36ms, 256.50ms]  71.88ms  84.61ms    7.55s       105 [100.10ms, 192.08ms] 113.90ms  20.65ms   11.96s
>             'fs_random':         1 [   9.09s,    9.09s]    9.09s   0.00ns    9.09s         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>       'fs_random_no_lp':         1 [   9.05s,    9.05s]    9.05s   0.00ns    9.05s         1 [  9.93ms,   9.93ms]   9.93ms   0.00ns   9.93ms
>         'graph_arc_lns':        25 [ 86.11ms,    1.43s] 698.21ms 487.03ms   17.46s        25 [ 20.00ns, 100.54ms]  58.10ms  47.71ms    1.45s
>         'graph_cst_lns':        23 [ 64.79ms,    1.97s] 711.64ms 570.27ms   16.37s        23 [ 10.00ns, 100.68ms]  57.91ms  48.30ms    1.33s
>         'graph_dec_lns':        23 [ 67.70ms,    1.67s] 681.12ms 554.61ms   15.67s        23 [ 10.00ns, 100.37ms]  56.58ms  49.63ms    1.30s
>         'graph_var_lns':        46 [ 77.13ms, 949.49ms] 330.33ms 242.13ms   15.20s        42 [ 10.00ns, 100.37ms]  31.04ms  44.27ms    1.30s
>                    'ls':       147 [  5.85ms, 161.63ms]  60.55ms  58.49ms    8.90s       147 [100.28ms, 216.86ms] 116.15ms  16.21ms   17.07s
>                'ls_lin':       148 [  5.59ms, 165.62ms]  65.56ms  59.58ms    9.70s       147 [ 60.51ms, 134.16ms] 114.40ms  14.91ms   16.82s
>                'max_lp':         1 [  49.29s,   49.29s]   49.29s   0.00ns   49.29s         1 [   7.94s,    7.94s]    7.94s   0.00ns    7.94s
>                 'no_lp':         1 [  49.31s,   49.31s]   49.31s   0.00ns   49.31s         1 [   3.67s,    3.67s]    3.67s   0.00ns    3.67s
>          'pseudo_costs':         1 [  49.35s,   49.35s]   49.35s   0.00ns   49.35s         1 [  13.09s,   13.09s]   13.09s   0.00ns   13.09s
>         'quick_restart':         1 [  49.35s,   49.35s]   49.35s   0.00ns   49.35s         1 [   7.35s,    7.35s]    7.35s   0.00ns    7.35s
>   'quick_restart_no_lp':         1 [  49.35s,   49.35s]   49.35s   0.00ns   49.35s         1 [   3.52s,    3.52s]    3.52s   0.00ns    3.52s
>         'reduced_costs':         1 [  49.35s,   49.35s]   49.35s   0.00ns   49.35s         1 [  13.53s,   13.53s]   13.53s   0.00ns   13.53s
>             'rins/rens':       122 [  8.92ms,    2.02s] 123.08ms 386.51ms   15.02s        14 [148.10us, 101.35ms]  73.19ms  43.53ms    1.02s
>           'rnd_cst_lns':        25 [ 95.14ms,    1.31s] 611.77ms 407.21ms   15.29s        25 [ 10.00ns, 100.20ms]  59.01ms  46.82ms    1.48s
>           'rnd_var_lns':        35 [ 98.99ms, 875.25ms] 476.20ms 235.21ms   16.67s        35 [ 10.00ns, 100.39ms]  59.04ms  45.76ms    2.07s
>      'routing_path_lns':        21 [264.33ms,    1.34s] 756.46ms 350.75ms   15.89s        21 [ 90.48us, 100.31ms]  57.89ms  45.40ms    1.22s
>    'routing_random_lns':        19 [409.56ms,    1.15s] 838.01ms 275.13ms   15.92s        19 [ 11.74us, 100.24ms]  67.13ms  41.26ms    1.28s
> 
> Search stats               Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  26'947        721   261'027    43'355  13'396'233     14'793'340
>            'default_lp':  26'941        299   267'416    41'446   9'877'453     11'991'125
>             'fs_random':  26'941          0    22'856    22'856   3'513'979      3'863'969
>       'fs_random_no_lp':  26'941          0    26'339    26'185   4'052'739      4'345'780
>                'max_lp':  26'942         25    33'520    26'184   4'078'617      4'520'060
>                 'no_lp':  26'941      1'074   328'003    39'896  13'165'644     16'034'489
>          'pseudo_costs':  26'941         50    41'345    26'945   4'606'839      5'399'442
>         'quick_restart':  26'960         96   208'140    43'174  10'310'049     12'890'358
>   'quick_restart_no_lp':  26'964        825   500'374    39'962  10'340'792     13'283'282
>         'reduced_costs':  26'941        119   260'126    35'315   6'816'163      9'302'693
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':           439     597'484     182'235             0         9       947     107'603         0         32          144       23
>            'default_lp':            15         391       3'404             0         0       720     107'066         0         15           60        0
>             'fs_random':             0           0           0             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':             0           0           0             0         0         0           0         0          0            0        0
>                'max_lp':             2          25         915             0         0         0           0         0          0            0        0
>                 'no_lp':           657      93'972     399'402             0         1       712     107'047         0          2            9        0
>          'pseudo_costs':             3          64         998             0         0         0           0         0          0            0        0
>         'quick_restart':            46      16'102      63'294             0         1       704     107'028         0          0            0        0
>   'quick_restart_no_lp':           309      95'791     226'213             0         0       712     107'050         0          4           16        0
>         'reduced_costs':             5          36       2'116             0         0       767     107'143         0         16           73       23
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':          9      43'349          0    6'093       41        0
>       'fs_random':          9           0          0        0        0        0
>          'max_lp':          1      10'967      1'027      465        3        0
>    'pseudo_costs':          1      26'095      1'565      959        1        0
>   'quick_restart':          9      35'784          0    3'518       20        1
>   'reduced_costs':          1      31'487      1'263      491       21        0
> 
> Lp dimension             Final dimension of first component
>      'default_lp':   350 rows, 26933 columns, 53564 entries
>       'fs_random':         0 rows, 26933 columns, 0 entries
>          'max_lp':   808 rows, 27108 columns, 57965 entries
>    'pseudo_costs':  1058 rows, 27108 columns, 57060 entries
>   'quick_restart':   351 rows, 26933 columns, 53715 entries
>   'reduced_costs':   977 rows, 27108 columns, 71382 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0     468         0  15'332           0
>    'pseudo_costs':          0            0     957         0   7'949           0
>   'quick_restart':          0            0       4         0       0           0
>   'reduced_costs':          0            0     509         0   7'945           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':          519        0        0     352          0      0             0          0/0
>       'fs_random':          519        0        0     352          0      0             0          0/0
>          'max_lp':       68'763       55        0     352          0      0         4'256  1'027/1'877
>    'pseudo_costs':       69'301       29        0     352          0      0         1'155  1'565/2'664
>   'quick_restart':          519        0        0     352          0      0             0          0/0
>   'reduced_costs':       68'999      104        0     352          0      2         2'567  1'263/2'071
> 
> Lp Cut            max_lp  reduced_costs  pseudo_costs
>           CG_FF:      16             28            32
>            CG_K:      12             21            18
>            CG_R:      16             12            20
>           CG_RB:      14             19            21
>          CG_RBP:       1              3             4
>         Circuit:      18             76            43
>    CircuitExact:       -              -             1
>          Clique:       4              5             9
>              IB:     179            605           907
>        MIR_1_FF:      75             47            90
>         MIR_1_K:       4              1             2
>        MIR_1_RB:     114             56            53
>       MIR_1_RBP:      61             22            16
>        MIR_2_FF:      36             33            43
>         MIR_2_K:       3              -             1
>         MIR_2_R:       -              2             4
>        MIR_2_RB:      31             34            29
>       MIR_2_RBP:      14             16             9
>        MIR_3_FF:      25             15            30
>         MIR_3_K:       -              2             1
>        MIR_3_KL:       1              -             -
>         MIR_3_R:       2              7             3
>        MIR_3_RB:      26             21            21
>       MIR_3_RBP:       7              6             9
>        MIR_4_FF:      20             17            26
>         MIR_4_K:       -              1             2
>         MIR_4_R:       1              6             3
>        MIR_4_RB:      27             24            14
>       MIR_4_RBP:       5              6             5
>        MIR_5_FF:       6             16            23
>         MIR_5_K:       -              1             2
>         MIR_5_R:       2              6             1
>        MIR_5_RB:      11             31             7
>       MIR_5_RBP:       2             10             4
>        MIR_6_FF:      13             20            17
>         MIR_6_K:       -              -             2
>         MIR_6_R:       2              5             2
>        MIR_6_RB:      14             13            11
>       MIR_6_RBP:       7              5             6
>    ZERO_HALF_FF:      35              3             9
>     ZERO_HALF_K:       1              -             1
>     ZERO_HALF_R:     160             58            43
>    ZERO_HALF_RB:      48              9            18
>   ZERO_HALF_RBP:      14              1             3
> 
> LNS stats                Improv/Calls  Closed  Difficulty  TimeLimit
>        'graph_arc_lns':          4/25     44%    2.19e-01       0.10
>        'graph_cst_lns':          3/23     43%    2.67e-01       0.10
>        'graph_dec_lns':          6/23     43%    2.69e-01       0.10
>        'graph_var_lns':          4/42     71%    9.97e-01       0.10
>            'rins/rens':         11/15     33%    5.16e-02       0.10
>          'rnd_cst_lns':          4/25     44%    2.39e-01       0.10
>          'rnd_var_lns':          7/35     49%    5.63e-01       0.10
>     'routing_path_lns':          5/21     48%    2.08e-01       0.10
>   'routing_random_lns':          5/19     42%    1.68e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':        5                  3     1'462         0              0          0             26        872'694
>                     'fj_restart_compound':        1                  1         0        12              1          0              0            360
>                 'fj_restart_compound_obj':       25                  8         0       314            233          0              0          9'699
>             'fj_restart_compound_perturb':       18                  7         0       101             94          0              0          8'535
>         'fj_restart_compound_perturb_obj':       11                  7         0        48             44          0              0          5'102
>                        'fj_restart_decay':        5                  4     1'637         0              0          0             20        757'622
>               'fj_restart_decay_compound':       10                  3         0       108             69          0              0          3'867
>           'fj_restart_decay_compound_obj':       12                  6         0       178            153          0              0          4'500
>       'fj_restart_decay_compound_perturb':       18                  5         0       105            101          0              0          8'737
>   'fj_restart_decay_compound_perturb_obj':       10                  9         0        66             56          0              0          4'509
>                    'fj_restart_decay_obj':       21                  7     7'048         0              0          0             93      3'771'763
>                'fj_restart_decay_perturb':        5                  3     1'716         0              0          0              6        771'411
>            'fj_restart_decay_perturb_obj':       10                  7     3'381         0              0          0              8      1'384'315
>                          'fj_restart_obj':        7                  6     2'060         0              0          0             29      1'079'313
>                      'fj_restart_perturb':        6                  3     1'954         0              0          0              9      1'009'931
>                  'fj_restart_perturb_obj':       29                  4     9'086         0              0          0            110      6'471'187
>                          'ls_lin_restart':       20                 20     2'522         0              0          0          1'283        600'815
>                 'ls_lin_restart_compound':       19                 19         0        36              0         18              0          8'498
>         'ls_lin_restart_compound_perturb':       17                 17         0        34              0         17              0          8'014
>                    'ls_lin_restart_decay':       18                 18     2'448         0              0          0            700        804'361
>           'ls_lin_restart_decay_compound':       15                 14         0        30              0         15              0          7'059
>   'ls_lin_restart_decay_compound_perturb':       23                 22         0        46              0         23              0         10'843
>            'ls_lin_restart_decay_perturb':       22                 20     3'284         0              0          0            764      1'236'678
>                  'ls_lin_restart_perturb':       14                 14     1'896         0              0          0          1'013        432'546
>                              'ls_restart':       12                 11     1'509         0              0          0            766        355'978
>                     'ls_restart_compound':       24                 23         0        48              0         24              0         11'287
>             'ls_restart_compound_perturb':       22                 22         0        44              0         22              0         10'290
>                        'ls_restart_decay':       20                 20     2'847         0              0          0            798        926'116
>               'ls_restart_decay_compound':       18                 18         0        36              0         18              0          8'477
>       'ls_restart_decay_compound_perturb':       15                 14         0        32              0         16              0          7'353
>                'ls_restart_decay_perturb':       18                 18     2'556         0              0          0            697        838'623
>                      'ls_restart_perturb':       18                 17     2'282         0              0          0          1'146        554'292
> 
> Solutions (25)             Num     Rank
>        'fs_random_no_lp':    1    [1,1]
>          'graph_arc_lns':    3  [17,20]
>          'graph_cst_lns':    1  [22,22]
>          'graph_dec_lns':    6   [3,24]
>          'graph_var_lns':    3   [7,15]
>   'ls_lin_restart_decay':    1  [19,19]
>            'rnd_cst_lns':    3   [2,23]
>            'rnd_var_lns':    4   [5,21]
>       'routing_path_lns':    2   [6,25]
>     'routing_random_lns':    1  [10,10]
> 
> Objective bounds     Num
>   'initial_domain':    1
>     'pseudo_costs':    2
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':     52      769       45
>    'fj solution hints':     75        0       75
>         'lp solutions':  1'300       10      300
>                 'pump':    147      112
> 
> Clauses shared            Num
>                  'core':   86
>            'default_lp':   88
>                'max_lp':   19
>                 'no_lp':  264
>          'pseudo_costs':   18
>         'quick_restart':   23
>   'quick_restart_no_lp':  200
>         'reduced_costs':   66
> 
> CpSolverResponse summary:
> status: FEASIBLE
> objective: 144
> best_bound: 62
> integers: 26691
> booleans: 26941
> conflicts: 0
> branches: 26339
> propagations: 4052739
> integer_propagations: 4345780
> restarts: 26185
> lp_iterations: 0
> walltime: 60.0979
> usertime: 60.0979
> deterministic_time: 133.439
> gap_integral: 702.895
> solution_fingerprint: 0x77a614f658ddfa81
> 
> --- Condition (with 26 chars) ---
> str1: tkgnkuhmpxnhtqgxzvxis
> str2: iojiqfolnbxxcvsuqpvissbxf
> str3: ulcinycosovozpplp
> str4: igevazgbrddbcsvrvnngf
> str5: pyplrzxucpmqvgtdfuivcdsbo
> str6: pbdevdcvdpfzsmsbroqvbbh
> str7: enbczfjtvxerzbrvigple
> str8: rxwxqkrdrlctodtmprpxwd
> 
> --- Solution (of length 144) ---
>  Sol: ulcintykeignbczfjoskovuhmpyozppgexnhtvxearzgbdevdcvdpfzsmrsddbrvjiqfolcsnvrbxwxqcgkvsuqrplrzxucpmqvgtdissbfnnzruigvxicdsgpbflctodtmpropxqvwdebbh
> str1: -----t-k--gn-------k--uhmp-------xnht-----------------------------q--------------g----------x----------------z----vxi--s------------------------
> str2: ---i-------------o----------------------------------------------jiqfol--n--bx-x-c--vsuq-p---------v---issb---------x-------f--------------------
> str3: ulcin-y------c---os-ov-----ozpp--------------------------------------l------------------p-------------------------------------------------------
> str4: ---i------g---------------------e----v--a-zgb------------r-ddb--------cs-vr--------v-----------------------nn----g---------f--------------------
> str5: -------------------------py--p---------------------------------------l----r----------------zxucpmqvgtd----f----ui-v--cds--b----o----------------
> str6: -------------------------p------------------bdevdcvdpfzsm-s--br-----o----------q---v---------------------b----------------b--------------------h
> str7: --------e--nbczfj-------------------tvxe-rz-b------------r-----v-i---------------g------pl--------------------------------------------------e---
> str8: -----------------------------------------r----------------------------------xwxq--k----r-------------d--------r-------------lctodtmpr-px--wd----
> 
> example file name: 'uniform_q26n008k015-025.txt'
> best objective: 144
> best bound: 62.0
> wall time: 60.797524s
> ```

In [ ]:
```python
scsp.util.bench(Model, example_filename="uniform_q26n016k015-025.txt", log=True)
```

> ```
> 
> Starting CP-SAT solver v9.14.6206
> Parameters: max_time_in_seconds: 60 log_search_progress: true
> Setting number of workers to 12
> 
> Initial optimization model '': (model_fingerprint: 0x5107eee0b9c6d108)
> #Variables: 98'291 (#bools: 95'995 in objective) (98'291 primary variables)
>   - 97'967 Booleans in [0,1]
>   - 323 in [1,323]
>   - 1 constants in {0} 
> #kCircuit: 1
> #kLinear2: 98'258 (#enforced: 97'951)
> 
> Starting presolve at 0.03s
>   2.17e-02s  0.00e+00d  [DetectDominanceRelations] 
>   1.90e+00s  0.00e+00d  [PresolveToFixPoint] #num_loops=25 #num_dual_strengthening=1 
>   1.16e-03s  0.00e+00d  [ExtractEncodingFromLinear] 
>   5.10e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   2.05e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 295'162 nodes and 588'674 arcs.
> [Symmetry] Symmetry computation done. time: 0.0210727 dtime: 0.0450922
>   2.03e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.45e+00s  1.00e+00d *[Probe] #probed=15'272 #new_binary_clauses=12'757 
>   5.39e-04s  0.00e+00d  [MaxClique] 
>   2.16e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.97e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=2 #num_dual_strengthening=1 
>   1.09e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   1.99e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.03e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   9.15e-04s  1.84e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=307 
>   3.94e-02s  0.00e+00d  [DetectDifferentVariables] #different=307 
>   1.43e-03s  0.00e+00d  [ProcessSetPPC] 
>   1.50e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   1.91e-02s  1.94e-03d  [FindBigAtMostOneAndLinearOverlap] 
>   3.14e-02s  9.31e-03d  [FindBigVerticalLinearOverlap] 
>   9.43e-04s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   7.68e-04s  0.00e+00d  [MergeClauses] 
>   2.63e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.50e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.64e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.52e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.16e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   2.14e-02s  0.00e+00d  [DetectDuplicateConstraints] 
> [Symmetry] Graph for symmetry has 490'418 nodes and 881'558 arcs.
> [Symmetry] Symmetry computation done. time: 0.0908477 dtime: 0.155929
> [SAT presolve] num removable Booleans: 0 / 97967
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:48814 literals:97628 vars:97628 one_side_vars:97628 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00242779s] clauses:48814 literals:97628 vars:97628 one_side_vars:97628 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0032575s] clauses:48814 literals:97628 vars:97628 one_side_vars:97628 simple_definition:0 singleton_clauses:0
>   2.08e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.49e+00s  1.00e+00d *[Probe] #probed=15'270 #new_binary_clauses=5'283 
>   2.95e-01s  1.00e+00d *[MaxClique] 
>   2.77e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.68e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.30e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.60e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.20e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   1.62e-03s  1.84e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=307 
>   3.48e-02s  0.00e+00d  [DetectDifferentVariables] #different=307 
>   1.08e-02s  2.93e-04d  [ProcessSetPPC] #relevant_constraints=48'814 
>   2.67e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.69e-02s  1.17e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   3.26e-02s  9.80e-03d  [FindBigVerticalLinearOverlap] 
>   1.56e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   1.93e-03s  0.00e+00d  [MergeClauses] 
>   3.15e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.78e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   3.13e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.77e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   5.71e-03s  0.00e+00d  [DetectDuplicateColumns] 
>   3.56e-02s  0.00e+00d  [DetectDuplicateConstraints] #duplicates=48'814 
> [Symmetry] Graph for symmetry has 490'418 nodes and 881'558 arcs.
> [Symmetry] Symmetry computation done. time: 0.0909148 dtime: 0.155929
> [SAT presolve] num removable Booleans: 0 / 97967
> [SAT presolve] num trivial clauses: 0
> [SAT presolve] [0s] clauses:48814 literals:97628 vars:97628 one_side_vars:97628 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.0028714s] clauses:48814 literals:97628 vars:97628 one_side_vars:97628 simple_definition:0 singleton_clauses:0
> [SAT presolve] [0.00374531s] clauses:48814 literals:97628 vars:97628 one_side_vars:97628 simple_definition:0 singleton_clauses:0
>   2.44e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   3.50e+00s  1.00e+00d *[Probe] #probed=15'270 #new_binary_clauses=5'283 
>   3.00e-01s  1.00e+00d *[MaxClique] 
>   2.91e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.74e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   2.51e-02s  0.00e+00d  [ProcessAtMostOneAndLinear] 
>   2.74e-02s  0.00e+00d  [DetectDuplicateConstraints] 
>   2.36e-02s  0.00e+00d  [DetectDuplicateConstraintsWithDifferentEnforcements] 
>   2.57e-03s  1.84e-06d  [DetectDominatedLinearConstraints] #relevant_constraints=307 
>   3.47e-02s  0.00e+00d  [DetectDifferentVariables] #different=307 
>   1.20e-02s  2.93e-04d  [ProcessSetPPC] #relevant_constraints=48'814 
>   3.45e-03s  0.00e+00d  [FindAlmostIdenticalLinearConstraints] 
>   2.69e-02s  1.17e-02d  [FindBigAtMostOneAndLinearOverlap] 
>   3.26e-02s  9.80e-03d  [FindBigVerticalLinearOverlap] 
>   2.39e-03s  0.00e+00d  [FindBigHorizontalLinearOverlap] 
>   2.88e-03s  0.00e+00d  [MergeClauses] 
>   3.53e-02s  0.00e+00d  [DetectDominanceRelations] 
>   2.81e-01s  0.00e+00d  [PresolveToFixPoint] #num_loops=1 #num_dual_strengthening=1 
>   1.49e-02s  0.00e+00d  [ExpandObjective] 
> 
> Presolve summary:
>   - 0 affine relations were detected.
>   - rule 'TODO dual: only one blocking constraint?' was applied 881'847 times.
>   - rule 'deductions: 184507 stored' was applied 1 time.
>   - rule 'duplicate: removed constraint' was applied 48'814 times.
>   - rule 'incompatible linear: add implication' was applied 146'442 times.
>   - rule 'linear: reduced variable domains' was applied 3'189 times.
>   - rule 'presolve: 1 unused variables removed.' was applied 1 time.
>   - rule 'presolve: iteration' was applied 3 times.
>   - rule 'variables: detect half reified value encoding' was applied 16 times.
> 
> Presolved optimization model '': (model_fingerprint: 0x6c44100a00edf248)
> #Variables: 98'290 (#bools: 95'995 in objective) (98'290 primary variables)
>   - 97'967 Booleans in [0,1]
>   - 166 different domains in [1,323] with a largest complexity of 1.
> #kBoolAnd: 97'628 (#enforced: 97'628) (#literals: 195'256)
> #kCircuit: 1
> #kLinear1: 16 (#enforced: 16)
> #kLinear2: 98'242 (#enforced: 97'935)
> [Symmetry] Graph for symmetry has 490'417 nodes and 881'558 arcs.
> [Symmetry] Symmetry computation done. time: 0.0899753 dtime: 0.155929
> 
> Preloading model.
> #Bound  16.65s best:inf   next:[0,95995]  initial_domain
> #Model  16.70s var:98290/98290 constraints:195887/195887
> 
> Starting search at 16.71s with 12 workers.
> 8 full problem subsolvers: [core, default_lp, max_lp, no_lp, pseudo_costs, quick_restart, quick_restart_no_lp, reduced_costs]
> 4 first solution subsolvers: [fj(2), fs_random, fs_random_no_lp]
> 12 interleaved subsolvers: [feasibility_pump, graph_arc_lns, graph_cst_lns, graph_dec_lns, graph_var_lns, ls, ls_lin, rins/rens, rnd_cst_lns, rnd_var_lns, routing_path_lns, routing_random_lns]
> 3 helper subsolvers: [neighborhood_helper, synchronization_agent, update_gap_integral]
> 
> #Bound  32.80s best:inf   next:[47,95995] default_lp
> #Bound  33.35s best:inf   next:[49,95995] fs_random
> #Bound  33.47s best:inf   next:[62,95995] default_lp
> #Bound  34.07s best:inf   next:[69,95995] default_lp
> #Bound  39.17s best:inf   next:[70,95995] max_lp
> 
> Task timing                      n [     min,      max]      avg      dev     time         n [     min,      max]      avg      dev    dtime
>                  'core':         1 [  43.58s,   43.58s]   43.58s   0.00ns   43.58s         1 [   1.33s,    1.33s]    1.33s   0.00ns    1.33s
>            'default_lp':         1 [  43.35s,   43.35s]   43.35s   0.00ns   43.35s         1 [   3.56s,    3.56s]    3.56s   0.00ns    3.56s
>      'feasibility_pump':       309 [  3.91ms,    1.10s]  17.42ms  69.35ms    5.38s       201 [  2.46ms, 546.14ms]   5.29ms  38.29ms    1.06s
>                    'fj':       222 [ 10.76ms, 339.08ms] 114.27ms  88.34ms   25.37s       222 [ 53.17ms, 455.77ms] 123.33ms  46.62ms   27.38s
>                    'fj':       249 [ 10.62ms, 411.67ms] 100.01ms  86.59ms   24.90s       249 [100.26ms, 353.11ms] 125.10ms  42.88ms   31.15s
>             'fs_random':         1 [  43.20s,   43.20s]   43.20s   0.00ns   43.20s         1 [  13.33s,   13.33s]   13.33s   0.00ns   13.33s
>       'fs_random_no_lp':         1 [  43.35s,   43.35s]   43.35s   0.00ns   43.35s         1 [   2.16s,    2.16s]    2.16s   0.00ns    2.16s
>         'graph_arc_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_cst_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_dec_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>         'graph_var_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                    'ls':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                'ls_lin':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>                'max_lp':         1 [  43.52s,   43.52s]   43.52s   0.00ns   43.52s         1 [   5.28s,    5.28s]    5.28s   0.00ns    5.28s
>                 'no_lp':         1 [  42.18s,   42.18s]   42.18s   0.00ns   42.18s         1 [   1.20s,    1.20s]    1.20s   0.00ns    1.20s
>          'pseudo_costs':         1 [  43.35s,   43.35s]   43.35s   0.00ns   43.35s         1 [  11.11s,   11.11s]   11.11s   0.00ns   11.11s
>         'quick_restart':         1 [  43.35s,   43.35s]   43.35s   0.00ns   43.35s         1 [   3.21s,    3.21s]    3.21s   0.00ns    3.21s
>   'quick_restart_no_lp':         1 [  43.35s,   43.35s]   43.35s   0.00ns   43.35s         1 [   2.02s,    2.02s]    2.02s   0.00ns    2.02s
>         'reduced_costs':         1 [  43.35s,   43.35s]   43.35s   0.00ns   43.35s         1 [  13.37s,   13.37s]   13.37s   0.00ns   13.37s
>             'rins/rens':       191 [  3.28ms,    7.40s] 168.68ms 865.92ms   32.22s         3 [  1.37ms,  58.89ms]  21.75ms  26.31ms  65.24ms
>           'rnd_cst_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>           'rnd_var_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>      'routing_path_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
>    'routing_random_lns':         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns         0 [  0.00ns,   0.00ns]   0.00ns   0.00ns   0.00ns
> 
> Search stats               Bools  Conflicts  Branches  Restarts  BoolPropag  IntegerPropag
>                  'core':  97'983         14    16'594    13'586   4'456'304      4'746'879
>            'default_lp':  97'983         50    56'875    16'818   8'311'360      8'836'408
>             'fs_random':  97'983         50    47'658    13'569   4'244'362      4'516'758
>       'fs_random_no_lp':  97'983         50   192'324    17'378   8'433'654      9'002'050
>                'max_lp':  97'983          0    13'568    13'568   4'101'752      4'313'813
>                 'no_lp':  97'983         13    16'549    13'568   4'350'346      4'717'459
>          'pseudo_costs':  97'983          9    18'533    13'568   4'123'233      4'352'635
>         'quick_restart':  97'983         10   264'238    17'017   8'216'311      8'966'937
>   'quick_restart_no_lp':  97'983         10   153'460    17'242   8'332'689      8'811'606
>         'reduced_costs':  97'983          9    92'453    13'568   4'124'910      4'426'085
> 
> SAT stats                 ClassicMinim  LitRemoved  LitLearned  LitForgotten  Subsumed  MClauses  MDecisions  MLitTrue  MSubsumed  MLitRemoved  MReused
>                  'core':            12          90       1'849             0         0         0           0         0          0            0        0
>            'default_lp':             1          12         489             0         0         0           0         0          0            0        0
>             'fs_random':             2          24       1'312             0         0         0           0         0          0            0        0
>       'fs_random_no_lp':            16       7'726       5'601             0         0       558     168'307         0          0            0        0
>                'max_lp':             0           0           0             0         0         0           0         0          0            0        0
>                 'no_lp':            12          90       1'845             0         0         0           0         0          0            0        0
>          'pseudo_costs':             0           0          18             0         0         0           0         0          0            0        0
>         'quick_restart':             2           7       2'381             0         0       196      59'038         0          0            0        0
>   'quick_restart_no_lp':             2          17       1'149             0         0       415     125'055         0          0            0        0
>         'reduced_costs':             0           0          23             0         0         0           0         0          0            0        0
> 
> Lp stats            Component  Iterations  AddedCuts  OPTIMAL  DUAL_F.  DUAL_U.
>      'default_lp':         17       5'896          0      978        2        0
>       'fs_random':         17      31'207          0    1'070       38        0
>          'max_lp':          1       3'080      1'162        6        1        0
>    'pseudo_costs':          1      13'463        436      132        4        0
>   'quick_restart':         17       6'020          0      300        2        0
>   'reduced_costs':          1      21'670        414      122        5        0
> 
> Lp dimension                Final dimension of first component
>      'default_lp':     648 rows, 97967 columns, 195934 entries
>       'fs_random':     647 rows, 97967 columns, 195634 entries
>          'max_lp':  245763 rows, 98290 columns, 898123 entries
>    'pseudo_costs':    1554 rows, 98290 columns, 373630 entries
>   'quick_restart':     648 rows, 97967 columns, 195934 entries
>   'reduced_costs':    1652 rows, 98290 columns, 325271 entries
> 
> Lp debug            CutPropag  CutEqPropag  Adjust  Overflow     Bad  BadScaling
>      'default_lp':          0            0       0         0       0           0
>       'fs_random':          0            0       0         0       0           0
>          'max_lp':          0            0       7         0  17'294           0
>    'pseudo_costs':          0            0     132         0   2'756           0
>   'quick_restart':          0            0       0         0       0           0
>   'reduced_costs':          0            0     123         0   2'057           0
> 
> Lp pool             Constraints  Updates  Simplif  Merged  Shortened  Split  Strenghtened    Cuts/Call
>      'default_lp':          955        0        0     648          0      0             0          0/0
>       'fs_random':          955        0        0     648          0      0             0          0/0
>          'max_lp':      246'817       16        0     648          0      0         5'872  1'162/2'344
>    'pseudo_costs':      246'091       13        0     648          0      0             0      436/860
>   'quick_restart':          955        0        0     648          0      0             0          0/0
>   'reduced_costs':      246'069       27        0     648          0      0             0      414/748
> 
> Lp Cut            reduced_costs  pseudo_costs  max_lp
>           CG_FF:             11            11      18
>            CG_K:             11            11      15
>            CG_R:              -             -      12
>           CG_RB:              -             -       5
>          CG_RBP:              -             -       3
>         Circuit:             43            42       4
>          Clique:              3             3       4
>              IB:            295           276      98
>        MIR_1_FF:             22            36     137
>         MIR_1_K:              -             -      32
>        MIR_1_RB:              -             -     133
>       MIR_1_RBP:              -             -      55
>        MIR_2_FF:              9            16      49
>         MIR_2_K:              -             1       4
>        MIR_2_RB:              -             -      42
>       MIR_2_RBP:              -             -      12
>        MIR_3_FF:              5            12      30
>         MIR_3_K:              -             -       7
>         MIR_3_R:              -             -       2
>        MIR_3_RB:              -             -      26
>       MIR_3_RBP:              -             -      11
>        MIR_4_FF:              6             8      32
>         MIR_4_K:              1             1       3
>         MIR_4_R:              -             -       4
>        MIR_4_RB:              -             -      22
>       MIR_4_RBP:              -             -       6
>        MIR_5_FF:              5             8      24
>         MIR_5_K:              -             1       6
>         MIR_5_R:              -             -       3
>        MIR_5_RB:              -             -      21
>       MIR_5_RBP:              -             -      11
>        MIR_6_FF:              3            10      15
>         MIR_6_K:              -             -       1
>         MIR_6_R:              -             -       3
>        MIR_6_RB:              -             -      16
>       MIR_6_RBP:              -             -       3
>    ZERO_HALF_FF:              -             -      69
>     ZERO_HALF_K:              -             -      22
>     ZERO_HALF_R:              -             -     117
>    ZERO_HALF_RB:              -             -      58
>   ZERO_HALF_RBP:              -             -      27
> 
> LNS stats                Improv/Calls  Closed  Difficulty  TimeLimit
>        'graph_arc_lns':           0/0      0%    5.00e-01       0.10
>        'graph_cst_lns':           0/0      0%    5.00e-01       0.10
>        'graph_dec_lns':           0/0      0%    5.00e-01       0.10
>        'graph_var_lns':           0/0      0%    5.00e-01       0.10
>            'rins/rens':           5/5    100%    9.39e-01       0.10
>          'rnd_cst_lns':           0/0      0%    5.00e-01       0.10
>          'rnd_var_lns':           0/0      0%    5.00e-01       0.10
>     'routing_path_lns':           0/0      0%    5.00e-01       0.10
>   'routing_random_lns':           0/0      0%    5.00e-01       0.10
> 
> LS stats                                    Batches  Restarts/Perturbs  LinMoves  GenMoves  CompoundMoves  Bactracks  WeightUpdates  ScoreComputed
>                              'fj_restart':       40                 11     3'739         0              0          0             23      3'242'025
>                     'fj_restart_compound':       15                  9         0       109             61          0              0          1'884
>                 'fj_restart_compound_obj':       14                  7         0        77             50          0              0          1'698
>             'fj_restart_compound_perturb':       27                 17         0        41             39          0              0          4'582
>         'fj_restart_compound_perturb_obj':        9                  5         0        12             11          0              0          1'687
>                        'fj_restart_decay':       50                 19     4'960         0              0          0             14      2'402'754
>               'fj_restart_decay_compound':       27                 10         0       189            119          0              0          3'104
>           'fj_restart_decay_compound_obj':       30                 11         0       212            166          0              0          3'368
>       'fj_restart_decay_compound_perturb':       36                  9         0        58             58          0              0          6'693
>   'fj_restart_decay_compound_perturb_obj':       20                 13         0        29             27          0              0          4'051
>                    'fj_restart_decay_obj':       65                 10     6'743         0              0          0             38      7'132'909
>                'fj_restart_decay_perturb':       25                  5     2'680         0              0          0              4      2'201'134
>            'fj_restart_decay_perturb_obj':       38                 10     4'106         0              0          0              2      2'476'936
>                          'fj_restart_obj':       10                  8       970         0              0          0              0         55'139
>                      'fj_restart_perturb':       26                 13     2'873         0              0          0              0      1'348'106
>                  'fj_restart_perturb_obj':       39                 11     4'101         0              0          0              3      2'585'660
> 
> Objective bounds     Num
>       'default_lp':    3
>        'fs_random':    1
>   'initial_domain':    1
>           'max_lp':    1
> 
> Solution repositories    Added  Queried  Synchro
>   'feasible solutions':      0        0        0
>    'fj solution hints':    160        0      160
>         'lp solutions':    837       20       93
>                 'pump':    308      170
> 
> Clauses shared            Num
>            'default_lp':   16
>             'fs_random':   28
>       'fs_random_no_lp':   13
>                 'no_lp':    1
>          'pseudo_costs':    9
>         'quick_restart':    5
>   'quick_restart_no_lp':    5
>         'reduced_costs':    6
> 
> CpSolverResponse summary:
> status: UNKNOWN
> objective: 95995
> best_bound: 70
> integers: 96629
> booleans: 97983
> conflicts: 13
> branches: 16549
> propagations: 4350346
> integer_propagations: 4717459
> restarts: 13568
> lp_iterations: 0
> walltime: 60.3506
> usertime: 60.3506
> deterministic_time: 121.286
> gap_integral: 1333.3
> 
> --- Condition (with 26 chars) ---
> str01: tkgnkuhmpxnhtqgxzvxis
> str02: iojiqfolnbxxcvsuqpvissbxf
> str03: ulcinycosovozpplp
> str04: igevazgbrddbcsvrvnngf
> str05: pyplrzxucpmqvgtdfuivcdsbo
> str06: pbdevdcvdpfzsmsbroqvbbh
> str07: enbczfjtvxerzbrvigple
> str08: rxwxqkrdrlctodtmprpxwd
> str09: kkqafigqjwokkskrblg
> str10: lxxpabivbvzkozzvd
> str11: krifsavncdqwhzc
> str12: qaxudgqvqcewbfgijowwy
> str13: rsxqjnfpadiusiqbezhkohmg
> str14: iwshvhcomiuvddm
> str15: htxxqjzqbctbakn
> str16: xusfcfzpeecvwantfmgqzu
> 
> --- Solution not found ---
> 
> example file name: 'uniform_q26n016k015-025.txt'
> best objective: None
> best bound: 70.0
> wall time: 62.776599s
> ```

う～ん非常に良くない.
なんならただの線形計画問題としての定式化 `LINEAR_CPSAT` よりも悪い.
