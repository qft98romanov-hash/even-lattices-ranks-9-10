from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output'
for lang in ('RU','EN'):
    path=OUT/f'lattices_complete_{lang}.tex'
    source=path.read_text()
    fragment=(ROOT/'research_20261008/consequences'/f'structural_corollaries_{lang}.tex').read_text()
    fragment='\n'.join(line for line in fragment.splitlines() if not line.startswith('%'))+'\n'
    split=fragment.index(r'\begin{corollary}')
    structure,cluster=fragment[:split],fragment[split:]
    if lang=='EN':
        structure=structure.replace('Let $K$ be either of the two rank-ten equality lattices. Then:', 'Let $K$ be an even integral rank-ten lattice with $m(K)\\ge6$ and $d(K)=54675$. Then:')
        structure=structure.replace('After the global equality classification, the proposition applies to every\npositive-definite even integral rank-ten lattice of minimum at least $6$\nand determinant $54675$.', 'Theorem \\ref{thm:global10equality} supplies a copy of $\\sqrt3E_8$ in every such $K$.')
        structure=structure.replace('of norm', 'of squared norm').replace('has\nnorm at least', 'has\nsquared norm at least').replace('norm-six representative','representative of squared norm six')
        structure=structure.replace('In the displayed bases,', 'Every copy of $K_9$ in $K$ is automatically primitive: a proper saturation would be an even integral rank-nine lattice of minimum at least 6 and determinant smaller than $e_9(6)=21870$. Thus the count of three primitive sublattices is also the count of all sublattices isometric to $K_9$.\n\nIn the displayed bases,')
        structure='\\subsection{Intrinsic structure of every rank-ten minimizer}\n\n'+structure
        cluster=cluster.replace('Let $K$ be either rank-ten equality lattice', 'Let $K$ be any even integral rank-ten lattice with $m(K)\\ge6$ and $d(K)=54675$')
        cluster=cluster.replace('After the global equality classification, this conclusion covers all\ndeterminant-minimal rank-ten sections.', 'By Theorem \\ref{thm:global10equality}, this conclusion covers every determinant-minimal rank-ten section.')
        cluster=cluster.replace('Under the global equality classification, every such\nsection has the intrinsic structure above,', 'By Theorem \\ref{thm:global10equality}, every such section has the structure of Proposition \\ref{prop:intrinsic-rank-ten},')
        cluster=cluster.replace('in the established all-diameter cluster\ntable', 'in the all-diameter cluster table proving Theorem \\ref{thm:cluster10}')
        cluster=cluster.replace('Ambient minimum $6$ gives', 'Ambient minimum at least $6$ gives')
        cluster=cluster.replace('\\texttt{audit\\_two\\_types\\_and\\_cluster\\_gap.py}', '\\file{research_20261008/consequences/audit_two_types_and_cluster_gap.py}')
        cluster='\\subsection{Uniform density loss and the scope of the dimension-38 result}\n\n'+cluster
        insertion=r'\subsection{A new independent consequence for rank nine}'
        cluster_insertion=r'\section{Verified results for the rank-48 ambient lattices}'
        reproduction=r'\subsection{The precise remaining work}'
        newreproduction=r'''The new equality-boundary and structural verifiers are relative to the package root:
\begin{itemize}
\item \file{research_20261008/independent_review/check_equality_windows_and_recovered_prunes.py};
\item \file{research_20261008/independent_review/check_boundaries_by_quadratic_module.py};
\item \file{research_20261008/consequences/audit_two_types_and_cluster_gap.py}.
\end{itemize}
The first two extend the complete strict-search certificate to the equality window. The third independently verifies the two types, their intrinsic sublattices, and the quantitative cluster comparison. All use exact arithmetic. Run them with assertions enabled; the finite-module checker accepts \texttt{--workers 2}.

'''
    else:
        structure=structure.replace('Пусть $K$ принадлежит одному из двух типов равенства ранга десять. Тогда:', 'Пусть $K$ --- чётная целая решётка ранга 10 с $m(K)\\ge6$ и $d(K)=54675$. Тогда:')
        structure=structure.replace('После глобальной классификации равенства предложение применимо ко всем\nположительно определённым чётным целочисленным решёткам ранга десять\nс минимумом не менее $6$ и определителем $54675$.', 'Теорема \\ref{thm:global10equality} обеспечивает наличие копии $\\sqrt3E_8$ в каждой такой $K$.')
        structure=structure.replace('В предъявленных базисах', 'Любая копия $K_9$ в $K$ автоматически примитивна: в случае непримитивности её насыщение было бы чётной целой решёткой ранга 9 с минимумом не меньше 6 и определителем меньше $e_9(6)=21870$. Поэтому число трёх примитивных подрешёток одновременно равно числу всех подрешёток, изометричных $K_9$.\n\nВ предъявленных базисах')
        structure='\\subsection{Внутренняя структура каждого минимизатора ранга 10}\n\n'+structure
        cluster=cluster.replace('Пусть $K$ принадлежит одному из двух типов равенства ранга десять,', 'Пусть $K$ --- произвольная чётная целая решётка ранга 10 с $m(K)\\ge6$ и $d(K)=54675$,')
        cluster=cluster.replace('После глобальной классификации равенства результат охватывает все\nсечения ранга десять минимального определителя.', 'По теореме \\ref{thm:global10equality} результат охватывает все сечения ранга 10 минимального определителя.')
        cluster=cluster.replace('После глобальной классификации равенства\nкаждое такое сечение имеет описанную выше внутреннюю структуру,', 'По теореме \\ref{thm:global10equality} каждое такое сечение имеет структуру из предложения \\ref{prop:intrinsic-rank-ten},')
        cluster=cluster.replace('из десяти интервалов доказанной таблицы кластерных оценок', 'из десяти интервалов таблицы в доказательстве теоремы \\ref{thm:cluster10}')
        cluster=cluster.replace('Минимум объемлющей решётки $6$ обеспечивает', 'Минимум объемлющей решётки не меньше $6$ обеспечивает')
        cluster=cluster.replace('\\texttt{audit\\_two\\_types\\_and\\_cluster\\_gap.py}', '\\file{research_20261008/consequences/audit_two_types_and_cluster_gap.py}')
        cluster='\\subsection{Равномерная потеря плотности и область вывода для размерности 38}\n\n'+cluster
        insertion=r'\subsection{Новое независимое следствие для ранга 9}'
        cluster_insertion=r'\section{Что проверено для окружающих решёток ранга 48}'
        reproduction=r'\subsection{Точный оставшийся объём работы}'
        newreproduction=r'''Новые проверки границы равенства и структуры указаны относительно корня пакета:
\begin{itemize}
\item \file{research_20261008/independent_review/check_equality_windows_and_recovered_prunes.py};
\item \file{research_20261008/independent_review/check_boundaries_by_quadratic_module.py};
\item \file{research_20261008/consequences/audit_two_types_and_cluster_gap.py}.
\end{itemize}
Первые два файла продолжают полный сертификат строгого поиска на окно равенства. Третий независимо проверяет два типа, их внутренние подрешётки и количественное сравнение кластеров. Везде используется точная арифметика. Запускать с включёнными проверками \texttt{assert}; проверка конечных модулей допускает параметр \texttt{--workers 2}.

'''
    assert source.count(insertion)==source.count(cluster_insertion)==source.count(reproduction)==1
    source=source.replace(insertion,structure+'\n'+insertion)
    source=source.replace(cluster_insertion,cluster+'\n'+cluster_insertion)
    source=source.replace(reproduction,newreproduction+reproduction)
    path.write_text(source)
print('Both reports augmented with intrinsic structure and quantified cluster consequences.')
