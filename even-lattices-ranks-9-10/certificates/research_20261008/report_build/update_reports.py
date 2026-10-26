"""Create updated bilingual reports from the immutable 7 October versions.
Run only after the new mathematical claims have been released by the audit.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'research_20261008/report_build'
OUT=ROOT/'output'
changes={
'EN':[
('Among rank-ten lattices containing $\\sqrt3E_8$, the minimum determinant is $54675$, attained by exactly two nonisometric lattices. For both, every nontrivial antipode cluster of squared diameter $\\beta<6$ lowers the density at the guaranteed radius.',
'The rank-ten minimum is attained by exactly two nonisometric lattices, $K_{10}$ and $\\Kalt$. Every minimizer contains $\\sqrt3E_8$. Over every minimizing rank-ten section, every nontrivial antipode cluster of squared diameter $\\beta<6$ lowers the density at the guaranteed radius.'),
('The global rank-ten minimum is established. Its complete equality classification and the full classification of embeddings into rank 48 remain open.',
'The global rank-ten minimum and its complete equality classification are established. The full classification of embeddings into rank 48 remains open.'),
('The exact value is established: $e_{10}(6)=54675$. There are exactly two equality types in the subclass containing $\\sqrt3E_8$; equality outside it is not classified.',
'The exact value is $e_{10}(6)=54675$, and globally there are exactly two equality types, $K_{10}$ and $\\Kalt$. Both contain $\\sqrt3E_8$.'),
('Settled for every $\\beta<6$ over both minimal rank-ten types containing $\\sqrt3E_8$.',
'Settled for every $\\beta<6$ over every determinant-minimizing rank-ten section.'),
('This is a computer-assisted result with the inputs specified explicitly below. The two known examples $K_{10}$ and $\\Kalt$ attain the bound; a complete classification of the \\emph{global} equality cases does not follow from this search below the bound.',
'This is a computer-assisted result with the inputs specified explicitly below. The examples $K_{10}$ and $\\Kalt$ attain the bound. The strict search first proves the minimum; the additional equality-window computation in Theorem \\ref{thm:global10equality} then proves that these are all minimizers.'),
('\\subsection{Dependencies, reproducibility, and the classification boundary}',
'\\subsection{Dependencies and reproducibility of the strict bound}'),
('Thus the singleton cluster is strictly optimal at the guaranteed radius of the antipode construction. By Theorem~\\ref{thm:rank10e8}, this covers every minimizer in the rank-ten subclass containing $\\sqrt3E_8$.',
'Thus the singleton cluster is strictly optimal at the guaranteed radius of the antipode construction. The global classification in Theorem~\\ref{thm:global10equality} makes this conclusion valid for every even integral rank-ten lattice of minimum at least 6 and determinant 54675.'),
('\\item \\textbf{Global rank-ten equality.} The value $e_{10}(6)=54675$ is established; all lattices of this determinant must still be classified without assuming a copy of $\\sqrt3E_8$. The strict search does not cover the additional endpoints of the equality window.\n',''),
('The source manuscript studies sections of extremal even unimodular lattices of rank 48 and sphere packings in dimensions 38--43.',
'This confidential research report consolidates the results of 7 October 2026 and the completed equality analysis of 8 October 2026. It is a working mathematical report for preparing a later draft. The source manuscript studies sections of extremal even unimodular lattices of rank 48 and sphere packings in dimensions 38--43.'),
('\\section{A rank-nine gap and a preliminary rank-ten bound}',
'\\section{A rank-nine gap and a preliminary rank-ten bound}\n\nThe bounds in this section are retained as intermediate results with different dependency sets. The sharp current statements are Theorems \\ref{thm:e10exact} and \\ref{thm:global10equality}, together with Corollary \\ref{cor:spectrum9}. In particular, 31595 is no longer the best established lower bound.'),
],
'RU':[
('В подклассе ранга 10, содержащем $\\sqrt3E_8$, минимум равен $54675$ и достигается ровно двумя неизометричными решётками. Для обеих все нетривиальные антиподные кластеры с квадратом диаметра $\\beta<6$ ухудшают плотность при гарантированном радиусе.',
'Минимум ранга 10 достигается ровно двумя неизометричными решётками: $K_{10}$ и $\\Kalt$. Каждый минимизатор содержит $\\sqrt3E_8$. Над любым минимальным сечением ранга 10 все нетривиальные антиподные кластеры с квадратом диаметра $\\beta<6$ ухудшают плотность при гарантированном радиусе.'),
('Глобальный минимум ранга 10 установлен. Полная классификация его равенства и всех вложений в ранг 48 остаётся открытой.',
'Глобальный минимум ранга 10 и полная классификация его равенства установлены. Полная классификация вложений в ранг 48 остаётся открытой.'),
('Значение установлено: $e_{10}(6)=54675$. В подклассе с $\\sqrt3E_8$ ровно два типа равенства; вне этого подкласса равенство ещё не классифицировано.',
'Точное значение $e_{10}(6)=54675$; глобально имеется ровно два типа равенства, $K_{10}$ и $\\Kalt$. Оба содержат $\\sqrt3E_8$.'),
('Закрыта для всех $\\beta<6$ над обоими минимальными типами ранга 10, содержащими $\\sqrt3E_8$.',
'Закрыта для всех $\\beta<6$ над каждым сечением ранга 10, минимальным по определителю.'),
('Это компьютерно поддержанный результат с явно указанными ниже входами. Два известных примера $K_{10}$ и $\\Kalt$ достигают границы; полная классификация \\emph{глобальных} случаев равенства из данного строгого поиска не следует.',
'Это компьютерно поддержанный результат с явно указанными ниже входами. Примеры $K_{10}$ и $\\Kalt$ достигают границы. Сначала строгий поиск доказывает минимум; дополнительный расчёт окна равенства в теореме \\ref{thm:global10equality} затем доказывает, что других минимизаторов нет.'),
('\\subsection{Зависимости, воспроизводимость и граница классификации}',
'\\subsection{Зависимости и воспроизводимость строгой границы}'),
('Значит, одноточечный кластер строго оптимален при гарантированном радиусе антиподной конструкции. В силу теоремы \\ref{thm:rank10e8} это охватывает все минимизаторы подкласса ранга 10, содержащего $\\sqrt3E_8$.',
'Значит, одноточечный кластер строго оптимален при гарантированном радиусе антиподной конструкции. Глобальная классификация теоремы \\ref{thm:global10equality} распространяет этот вывод на каждую чётную целую решётку ранга 10 с минимумом не меньше 6 и определителем 54675.'),
('\\item \\textbf{Глобальное равенство в ранге 10.} Значение $e_{10}(6)=54675$ установлено; требуется классифицировать все решётки этого определителя без предположения о наличии $\\sqrt3E_8$. Строгий поиск не покрывает новые граничные значения окна равенства.\n',''),
('Исходная работа посвящена сечениям экстремальных чётных унимодулярных решёток ранга 48 и упаковкам в размерностях 38--43.',
'Этот конфиденциальный исследовательский отчёт объединяет результаты 7 октября 2026 года и завершённый анализ равенства от 8 октября 2026 года. Это рабочий математический текст для подготовки будущего черновика статьи. Исходная работа посвящена сечениям экстремальных чётных унимодулярных решёток ранга 48 и упаковкам в размерностях 38--43.'),
('\\section{Разрыв в ранге 9 и предварительная граница ранга 10}',
'\\section{Разрыв в ранге 9 и предварительная граница ранга 10}\n\nОценки этого раздела сохранены как промежуточные результаты с иными наборами предпосылок. Окончательные точные утверждения --- теоремы \\ref{thm:e10exact}, \\ref{thm:global10equality} и следствие \\ref{cor:spectrum9}. В частности, число 31595 уже не является лучшей установленной нижней границей.'),
]}
old_boundary={
'EN':r'The exact \emph{value} of the global minimum is established. Theorem \ref{thm:rank10e8} classifies exactly two equality cases only under the assumption that $\sqrt3E_8$ is present. The search in this section uses the strict window $D\le54672$; it does not classify additional lattices of determinant 54675 that contain no $\sqrt3E_8$. At equality, the upper windows increase to $d_9\le40056$, $d_8\le24676$, $d_7\le13940$, and $d_6\le6460$; these additional endpoints cannot be discarded on the strength of the large margin in the final exclusion of the strict search.',
'RU':r'Установлено точное \emph{значение} глобального минимума. В теореме \ref{thm:rank10e8} ровно два случая равенства классифицированы только при наличии $\sqrt3E_8$. Поиск настоящего раздела использует строгое окно $D\le54672$; дополнительные решётки определителя 54675, не содержащие $\sqrt3E_8$, этим поиском не классифицированы. При равенстве верхние окна увеличиваются до $d_9\le40056$, $d_8\le24676$, $d_7\le13940$, $d_6\le6460$; эти дополнительные концы нельзя отбросить на основании большого запаса в последнем отсечении строгого поиска.'}
for lang in ('RU','EN'):
    candidates=[OUT/f'lattices_{lang}.tex', ROOT/'prior_reports'/f'lattices_{lang}.tex', OUT/f'rank9_rank10_results_20261007_{lang}.tex']
    baseline=next((p for p in candidates if p.is_file()),None)
    assert baseline is not None, 'Missing historical source; delivered new .tex files compile independently.'
    source=baseline.read_text().replace('7 октября 2026','8 октября 2026').replace('7 October 2026','8 October 2026')
    for old,new in changes[lang]:
        assert source.count(old)==1,(lang,old[:120],source.count(old))
        source=source.replace(old,new)
    assert source.count(old_boundary[lang])==1
    source=source.replace(old_boundary[lang],(B/f'equality_completion_{lang}.tex').read_text())
    if lang=='RU':
        source=source.replace('с квадратом минимума не меньше 6 имеет определитель не меньше 54675',r'с $m(L)\ge6$ имеет определитель не меньше 54675')
    (OUT/f'lattices_complete_{lang}.tex').write_text(source)
print('Updated both reports; compile and visually review before release.')
