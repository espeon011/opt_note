# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "ortools==9.11.4210",
# ]
# ///

import marimo

__generated_with = "0.11.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# 崩壊スターレイル 教育部の難問""")
    return


@app.cell
def _():
    from ortools.sat.python import cp_model
    return (cp_model,)


@app.cell
def _(cp_model):
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, variables):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__variables = variables
            self.__solution_count = 0

        def on_solution_callback(self):
            self.__solution_count += 1
            for v in self.__variables:
                print(f"{v}={self.value(v)}", end=" ")
            print()

        @property
        def solution_count(self):
            return self.__solution_count
    return (VarArraySolutionPrinter,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## その 3""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 問題文

        > 数日前にレムスティーン家でタイヤを盗んだ犯人を見つけました。
        > 当時、シルバーメインは容疑者をジャック、クリス、エリックの3人に絞り込んでいました。3人は言い争って譲りません。
        > ジャックは「タイヤを盗んだのはクリスだ！」と言いました。
        > 頭のいいジェパードはすぐに犯人を察しました。
        > 自分の副官を試すため、ジェパードはすぐに誰が泥棒かを言わずに、「おかしいな。3人の中で泥棒だけが嘘をついてない」と言いました。
        > レムスティーン家の車のタイヤを盗んだのは一体誰でしょう？

        ### 解き方

        暗黙の了解として犯人は 1 人だけであるとする. 
        ジャックが犯人だとするとジェパードの発言から正直者のはずだが, ジャックは犯人はクリスであると主張しているため, 矛盾. 
        従ってジャックは犯人ではなく, ジェパ―ドの発言から嘘をついていることになる. 
        ジャックの発言は嘘であるためタイヤを盗んだのはクリスではなく, 残ったエリックが犯人となる. 

        仮に犯人が 1 人だけではなく, 1 人以上と条件を緩めた場合, 

        - 3 人とも犯人
        - ジャックとクリスが犯人でエリックは無実

        のパターンも存在する. 

        犯人が 0 人の場合も許すと全員が無実である(よって全員嘘つき)ような解も存在する.

        ### 定式化

        ジャック, クリス, エリックをそれぞれ $1$, $2$, $3$ とする. 

        - 決定変数
          - $x_i \in \{0, 1\}$ (for $i = 1, 2, 3$): $i$ は正直者
          - $y_i \in \{0, 1\}$ (for $i = 1, 2, 3$): $i$ は嘘つき
          - $z_i \in \{0, 1\}$ (for $i = 1, 2, 3$): $i$ は犯人
        - 制約条件
          - $x_i + y_i = 1$ (for $i = 1, 2, 3$): 正直者か嘘つきのどちらか一方
          - $x_1 = z_2$: ジャックはクリスが犯人だと主張している(以下の 2 つと同じ)
        	- $x_1 \le z_2$: ジャックが正直者ならクリスは犯人
        	- $y_1 \le 1 - z_2$: ジャックが嘘つきならクリスは犯人ではない
          - $z_i = x_i$ (for $i = 1, 2, 3$): 犯人だけが正直者(以下の 2 つと同じ)
        	- $z_i \le x_i$ (for $i = 1, 2, 3$): 犯人は嘘をついていない
        	- $1 - z_i \le y_i$ (for $i = 1, 2, 3$): 犯人以外は嘘をついている
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 実装""")
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _suspects = ['jack', 'chris', 'eric']
    _liar = {s: _model.new_bool_var(f'{s}_is_liar') for s in _suspects}
    _culprit = {s: _model.new_bool_var(f'{s}_is_culprit') for s in _suspects}
    _model.add(_culprit['chris'] == 1).only_enforce_if(_liar['jack'].negated())
    _model.add(_culprit['chris'] == 0).only_enforce_if(_liar['jack'])
    for _s in _suspects:
        _model.add(_culprit[_s] == 1 - _liar[_s])
    _model.add_exactly_one(list(_culprit.values()))
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter(list(_liar.values()) + list(_culprit.values()))
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 補足

        犯人が 1 人だけという仮定を外すと全員犯人の場合と, 犯人が 2 人いる場合と, 犯人がいない場合の解も出てくる.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## その 4""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 問題文

        > ハワード、フィリップ、ジョイスの3人のうち、1人は善人、1人は悪人、1人は嘘つきです。
        > 善人は事実しか言わず、悪人は嘘しか言いません。
        > 嘘つきは事実を言ったかと思えば、嘘を言うというように、何でも言います。
        > ある日、ジョイスが「フィリップは善人ではなく悪人だ」と言いました。
        > そしてフィリップは「ハワードとジョイスのどちらか1人は善人だ」と言いました。
        > 3人のうち、嘘つきは誰でしょうか？

        ### 解き方

        フィリップの発言に注目する. 
        フィリップが善人だとすると発言内容は事実であるはずだが, フィリップ以外にももう 1 人善人がいることになり, 矛盾. 
        フィリップが悪人だとすると発言内容は誤りであるはずだが, ハワードとジョイスは両方とも善人でないとなると今度は善人が 1 人もいなくなるので矛盾. 
        従って嘘つきはフィリップである. 
        ちなみにフィリップが嘘つきなのでジョイスの主張は誤りとなり, ジョイスが悪人で確定する. よってハワードが善人であることもわかる.

        ### 定式化

        ハワード, フィリップ, ジョイスをそれぞれ $1$, $2$, $3$ とする. 

        - 決定変数
          - $x_i \in \{0, 1\}$: (for $i = 1, 2, 3$): $i$ は善人
          - $y_i \in \{0, 1\}$: (for $i = 1, 2, 3$): $i$ は悪人
          - $z_i \in \{0, 1\}$: (for $i = 1, 2, 3$): $i$ は嘘つき
        - 制約条件
          - $x_i + y_i + z_i = 1$ (for $i = 1, 2, 3$): 善人か悪人か嘘つきのどれか
          - 善人は 1 人: $\sum_{i=1}^3 x_i = 1$
          - 悪人は 1 人: $\sum_{i=1}^3 y_i = 1$
          - 嘘つきは 1 人: $\sum_{i=1}^3 z_i = 1$
          - $x_3 \le 1 - x_2$ and $x_3 \le y_2$: ジョイスはフィリップが善人ではなく悪人であると主張している
          - $y_3 \le x_2 + (1 - y_2)$: ジョイスが悪人である場合, 上記の NOT が成立する. 
          - $x_2 \le x_1 + x_3$: フィリップはハワードとジョイスのどちらか 1 人は善人であると主張している
          - $y_2 \le 1 - x_1$ and $y_2 \le 1 - x_3$: フィリップが悪人である場合, 上記の NOT が成立する
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 実装""")
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _members = ['howard', 'philip', 'joyce']
    _good_guys = {m: _model.new_bool_var(f'{m}_is_goodguy') for m in _members}
    _bad_guys = {m: _model.new_bool_var(f'{m}_is_badguy') for m in _members}
    _liars = {m: _model.new_bool_var(f'{m}_is_liar') for m in _members}
    for _m in _members:
        _model.add_exactly_one([_good_guys[_m], _bad_guys[_m], _liars[_m]])
    _model.add_exactly_one(list(_good_guys.values()))
    _model.add_exactly_one(list(_bad_guys.values()))
    _model.add_exactly_one(list(_liars.values()))
    _model.add_bool_and([_good_guys['philip'].negated(), _bad_guys['philip']]).only_enforce_if(_good_guys['joyce'])
    _model.add_bool_or([_good_guys['philip'], _bad_guys['philip'].negated()]).only_enforce_if(_bad_guys['joyce'])
    _model.add_bool_or([_good_guys['howard'], _good_guys['joyce']]).only_enforce_if(_good_guys['philip'])
    _model.add_bool_and([_good_guys['howard'].negated(), _good_guys['joyce'].negated()]).only_enforce_if(_bad_guys['philip'])
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter(list(_good_guys.values()) + list(_bad_guys.values()) + list(_liars.values()))
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 補足

        ハワードが善人, ジョイスが悪人, フィリップが嘘つきという解しかないことがわかる.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## その 7""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 問題文

        > 人目のつかない雪原の片隅に、古代の宝物が隠されているといわれています。
        > 探検家~~サンポ~~青髪のイケメンは数々の苦労を乗り越え、ついにその宝が隠された秘密の場所を見つけました。
        > そこには言葉を話す2つの扉がありました。
        > 1つは金の扉、もう1つは銀の扉です。
        > その2つの扉のうち、片方の扉は真実を話しますが、もう片方の扉は嘘しか言いません。
        > 片方の扉の奥には財宝があり、もう片方の扉の奥には古代のモンスターがいます。
        > 宝の地図によると、2つの扉は1つの質問にしか答えてくれません。
        > 頭のいい~~サンポ~~青髪のイケメンはしばらく考えこんだ末に、銀の扉に向かって「金の扉はあなたの奥に何があると言いますか？」と聞きました。
        > 銀の扉は「この後ろにあるのは財宝であると言うのだろう」と答えました。
        > ~~サンポ~~青髪のイケメンはどちらの扉を開けるでしょうか？

        ### 解き方

        金の扉が真実を話す場合, 銀の扉は嘘しか言わなくなる. 

        - 銀の扉の後ろに財宝がある場合
          - 金の扉(真実)「銀の扉の後ろには財宝がある」
          - 銀の扉(嘘)「『この後ろには古代のモンスターがいる』と言うだろう」
        - 銀の扉の後ろに古代のモンスターがいる場合
          - 金の扉(真実)「銀の扉の後ろには古代のモンスターがいる」
          - 銀の扉(嘘)「『この後ろには財宝がある』と言うだろう」

        金の扉が嘘しか言わない場合, 銀の扉は真実を話すことになる. 

        - 銀の扉の後ろに財宝がある場合
          - 金の扉(嘘)「銀の扉の後ろには古代のモンスターがいる」
          - 銀の扉(真実)「『この後ろには古代のモンスターがいる』と言うだろう」
        - 銀の扉の後ろに古代のモンスターがいる場合
          - 金の扉(嘘)「銀の扉の後ろには財宝がある」
          - 銀の扉(真実)「『この後ろには財宝がある』と言うだろう」

        銀の扉は金の扉が「後ろに財宝がある」と主張すると言っているので銀の扉の後ろには古代のモンスターがおり, 金の扉の後ろに財宝がある. 

        一般に $A$ と $B$ のどちらか一方が正直者でどちらか一方が嘘つきである場合, Yes か No で回答する質問 $X$ に対して「 $A$ は $X$ に Yes と回答するか? 」と $B$ に聞くと $X$ についての事実と逆の回答が返ってくる. (嘘つきの回答を丁度 1 回経由するため)

        今回 $X$ は「銀の扉の後ろに財宝があるか」で, 回答は Yes であったため実際は No であり銀の扉の後ろに財宝はない.

        ### 定式化

        金の扉, 銀の扉をそれぞれ $1$, $2$ とする. 

        - 決定変数
          - $x_i \in \{0, 1\}$ (for $i = 1, 2$): $i$ は真実を話す
          - $y_i \in \{0, 1\}$ (for $i = 1, 2$): $i$ は嘘を話す
          - $v_i \in \{0, 1\}$ (for $i = 1, 2$): $i$ の後ろには財宝がある
          - $w_i \in \{0, 1\}$ (for $i = 1, 2$): $i$ の後ろには古代のモンスターがいる
          - $s \in \{0, 1\}$: 金の扉は銀の扉の後ろには財宝があると主張する
          - $t \in \{0, 1\}$: 金の扉は銀の扉の後ろには古代のモンスターがいると主張する
          - $p \in \{0, 1\}$: 銀の扉は「金の扉が銀の扉の後ろに財宝があると言う」と主張する
          - $q \in \{0, 1\}$: 銀の扉は「金の扉が銀の扉の後ろにモンスターがいると言う」と主張する
        - 制約条件
          - $x_i + y_i = 1$ (for $i = 1, 2$): 真実を話すか嘘を話すかどちらか一方
          - 片方は真実を話し, 片方は嘘を話す: $\sum_{i=1}^2 x_i = 1 \quad \text{and} \quad \sum_{i=1}^2 y_i = 1$
          - $v_i + w_i = 1$ (for $i = 1, 2$): 扉の後ろには財宝かモンスターのどちらか一方がある
          - 片方の後ろには財宝があり, 片方の後ろにはモンスターがいる: $\sum_{i=1}^2 v_i = 1 \quad \text{and} \quad \sum_{i=1}^2 w_i = 1$
          - $s + t = 1$: 金の扉の主張はどちらか一方のみ
          - $x_1 + v_2 \le 1 + s$: 金の扉が正直者で銀の扉の後ろに財宝があればそのように主張する
          - $x_1 + w_2 \le 1 + t$: 金の扉が正直者で銀の扉の後ろにモンスターがいればそのように主張する
          - $y_1 + v_2 \le 1 + t$: 金の扉が嘘つきで銀の扉の後ろに財宝があれば逆の主張する
          - $y_1 + w_2 \le 1 + s$: 金の扉が嘘つきで銀の扉の後ろにモンスターがいれば逆の主張する
          - $p + q = 1$: 銀の盾の主張はどちらか一方のみ
          - $x_2 + s \le 1 + p$: 銀の扉が正直者であれば金の扉が「銀の扉の後ろには財宝がある」と言うであろうことをそのまま伝える
          - $x_2 + t \le 1 + q$: 銀の扉が正直者であれば金の扉が「銀の扉の後ろにはモンスターがいる」と言うであろうことをそのまま伝える
          - $y_2 + s \le 1 + q$: 銀の扉が嘘つきであれば金の扉が「銀の扉の後ろには財宝がある」と言うであろう場合逆のことを話す
          - $y_2 + t \le 1 + p$: 銀の扉が嘘つきであれば金の扉が「銀の扉の後ろにはモンスターがいる」と言うであろう場合逆のことを話す
          - $p = 1$: 銀の扉は「(金の扉は)この後ろにあるのは財宝であると言うのだろう」と答えた
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### 実装""")
    return


@app.cell
def _(VarArraySolutionPrinter, cp_model):
    _model = cp_model.CpModel()
    _gates = ['gold', 'silver']
    _honests = {g: _model.new_bool_var(f'{g}_gate_is_honest') for g in _gates}
    _liars = {g: _honests[g].negated() for g in _gates}
    _model.add_exactly_one(list(_honests.values()))
    _treasures = {g: _model.new_bool_var(f'{g}_gate_has_treasure') for g in _gates}
    _monsters = {g: _treasures[g].negated() for g in _gates}
    _model.add_exactly_one(list(_treasures.values()))
    _silver_says_gold_says = _model.new_bool_var('silver_says_gold_says_silver_has_treasure')
    _model.add(_silver_says_gold_says == 1)
    _gold_says = _model.new_bool_var('gold_says_silver_has_treasure')
    _model.add(_gold_says == _silver_says_gold_says).only_enforce_if(_honests['silver'])
    _model.add(_gold_says.negated() == _silver_says_gold_says).only_enforce_if(_liars['silver'])
    _model.add(_treasures['silver'] == _gold_says).only_enforce_if(_honests['gold'])
    _model.add(_treasures['silver'].negated() == _gold_says).only_enforce_if(_liars['gold'])
    _solver = cp_model.CpSolver()
    _solution_printer = VarArraySolutionPrinter(list(_honests.values()) + list(_treasures.values()))
    _solver.parameters.enumerate_all_solutions = True
    _status = _solver.solve(_model, _solution_printer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 補足

        2 つの実行可能解が存在するが, 
        金の扉と銀の扉が嘘つきであろうとと財宝のありかは変わらない.
        """
    )
    return


if __name__ == "__main__":
    app.run()
