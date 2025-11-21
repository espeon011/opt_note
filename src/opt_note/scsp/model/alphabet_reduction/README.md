# アルファベットアルゴリズムから不要なものを削る[^1]

アルファベットアルゴリズムで作成した解を $(c_1 c_2 \dots c_q)^k$ とする. 
各文字列 $s_i$ の $j$ 番目の文字はこの $(c_1 c_2 \dots c_q)^k$ の中の $j$ 番目のブロック ($1 \leq j \leq k$) がカバーすることになるが,
アルファベットアルゴリズムで構築した解において各ブロックはインスタンスに出現する全ての文字を並べて作られているため, 
$j$ 番目のブロックにはどの文字列の $j$ 番目の文字でもない文字が含まれている可能性がある. 
このような文字は捨てることで解を少し改善する.
しかし文字列の数が増えると削れる文字が少なくなり, 長さ $qk$ に近づく. 

[^1]: Paolo Barone, Paola Bonizzoni, Gianluca Delta Vedova, and Giancarlo Mauri. 2001. An approximation algorithm for the shortest common supersequence problem: an experimental analysis. In Proceedings of the 2001 ACM symposium on Applied computing (SAC '01). Association for Computing Machinery, New York, NY, USA, 56–60. https://doi.org/10.1145/372202.372275
