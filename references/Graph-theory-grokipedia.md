Graph theory  
Graph theory is a branch of discrete mathematics that studies graphs, which are abstract mathematical structures consisting of a set of vertices (or nodes) representing objects and a set of edges connecting pairs of vertices to model relations between those objects.\[1\] A graph   
𝐺  
G is formally defined as an ordered triple   
(  
𝑉  
(  
𝐺  
)  
,  
𝐸  
(  
𝐺  
)  
,  
𝜓  
𝐺  
)  
(V(G),E(G),ψ   
G  
​  
 ), where   
𝑉  
(  
𝐺  
)  
V(G) is a nonempty finite set of vertices,   
𝐸  
(  
𝐺  
)  
E(G) is a finite set of edges disjoint from   
𝑉  
(  
𝐺  
)  
V(G), and   
𝜓  
𝐺  
ψ   
G  
​  
  is an incidence function mapping each edge to an unordered pair of vertices (which may be the same for loops).\[1\] Graphs can be undirected (edges without direction), directed (digraphs with oriented edges), simple (no loops or multiple edges), or more general forms like multigraphs and pseudographs.\[2\]\[3\]  
The origins of graph theory trace back to 1736, when Leonhard Euler addressed the Seven Bridges of Königsberg problem, abstracting the city's bridge network into a graph to determine if a closed walk could traverse each bridge exactly once—an impossibility due to vertices of odd degree.\[3\] Euler's paper, "Solutio problematis ad geometriam situs pertinentis," marked the field's birth, initially applied to recreational puzzles like map coloring and later formalized in the 19th century through works on electrical networks and chemical structures.\[3\]\[4\] Key early developments include the degree-sum formula, stating that the sum of all vertex degrees equals twice the number of edges, and characterizations of Eulerian circuits in connected graphs where all degrees are even.\[2\]  
Graph theory has evolved into a cornerstone of modern mathematics and science, with profound applications across disciplines.\[5\] In computer science, it enables algorithms for shortest paths (e.g., Dijkstra's), network optimization, and web ranking via Google's PageRank, which models the internet as a directed graph to assess page importance based on link structures.\[6\] In biology and chemistry, graphs represent molecular bonds and genetic interactions; in transportation, they optimize routes and traffic flows; and in social sciences, they analyze networks of relationships.\[7\]\[8\] Notable theorems include the Four Color Theorem, proving that any planar graph (embeddable in a plane without edge crossings) is 4-colorable for vertex coloring without adjacent same-color vertices, and Kuratowski's theorem characterizing non-planar graphs.\[2\] Spectral graph theory further extends applications to data mining, machine learning, and scientific computing through eigenvalue analysis of adjacency matrices.\[9\]  
Fundamentals  
Undirected Graphs  
An undirected graph is a fundamental structure in graph theory, modeling pairwise relations between objects without implying directionality. It consists of a set of vertices connected by edges that are bidirectional, representing symmetric relationships such as friendships in a social network or roads between cities. Unlike more specialized variants, undirected graphs form the basis for many theoretical and applied problems in combinatorics, computer science, and optimization.\[10\]  
Formally, an undirected graph   
𝐺  
G is defined as an ordered pair   
𝐺  
\=  
(  
𝑉  
,  
𝐸  
)  
G=(V,E), where   
𝑉  
V is a set of vertices (also called nodes) and   
𝐸  
E is a set of edges, with each edge being an unordered pair   
{  
𝑢  
,  
𝑣  
}  
{u,v} where   
𝑢  
,  
𝑣  
∈  
𝑉  
u,v∈V and typically   
𝑢  
≠  
𝑣  
u  
\=v. A simple undirected graph restricts   
𝐸  
E to contain no loops (edges where   
𝑢  
\=  
𝑣  
u=v) and no multiple edges between the same pair of vertices, ensuring each possible connection appears at most once. In contrast, multigraphs allow multiple edges between the same pair, while pseudographs permit loops, which connect a vertex to itself and contribute twice to its degree in counting incidences. The degree   
𝑑  
(  
𝑣  
)  
d(v) of a vertex   
𝑣  
v is the number of edges incident to it, counting loops as two incidences. A key property is the handshaking lemma, which states that the sum of all vertex degrees equals twice the number of edges:  
∑  
𝑣  
∈  
𝑉  
𝑑  
(  
𝑣  
)  
\=  
2  
∣  
𝐸  
∣  
.  
v∈V  
∑  
​  
 d(v)=2∣E∣.  
This lemma arises because each edge contributes to the degree of exactly two vertices (or twice to one in the case of a loop).\[11\]\[12\]\[13\]\[14\]  
Common examples illustrate these concepts. The complete graph   
𝐾  
𝑛  
K   
n  
​  
  on   
𝑛  
n vertices connects every pair of distinct vertices with exactly one edge, resulting in   
𝑛  
(  
𝑛  
−  
1  
)  
2  
2  
n(n−1)  
​  
  edges and every vertex having degree   
𝑛  
−  
1  
n−1. The empty graph (also called the null or edgeless graph) on   
𝑛  
n vertices has   
∣  
𝑉  
∣  
\=  
𝑛  
∣V∣=n but   
∣  
𝐸  
∣  
\=  
0  
∣E∣=0, so all degrees are zero. The path graph   
𝑃  
𝑛  
P   
n  
​  
  consists of   
𝑛  
n vertices arranged in a sequence with edges only between consecutive vertices, forming a chain of   
𝑛  
−  
1  
n−1 edges where the endpoints have degree 1 and internal vertices have degree 2\. Graphs may be finite, with both   
𝑉  
V and   
𝐸  
E finite sets, or infinite, extending indefinitely in vertices or edges, which introduces complexities in analysis such as connectivity over unbounded structures. Additionally, graphs can be labeled, assigning distinct identifiers to vertices for explicit distinction, or unlabeled, treated up to isomorphism where only the structural relations matter. Directed graphs extend this model by orienting edges to indicate asymmetry, but undirected graphs remain central for symmetric interactions.\[15\]\[16\]\[17\]\[18\]\[19\]  
Directed Graphs  
A directed graph, also known as a digraph, extends the concept of an undirected graph by assigning a direction to each edge, thereby modeling asymmetric relationships such as one-way streets or dependencies in a process.\[20\]\[21\] Formally, a directed graph   
𝐺  
\=  
(  
𝑉  
,  
𝐴  
)  
G=(V,A) consists of a finite set   
𝑉  
V of vertices and a set   
𝐴  
A of ordered pairs   
(  
𝑢  
,  
𝑣  
)  
(u,v) with   
𝑢  
,  
𝑣  
∈  
𝑉  
u,v∈V, where each ordered pair is called an arc or directed edge from   
𝑢  
u to   
𝑣  
v.\[21\]\[22\] Unlike undirected graphs, arcs in a digraph are not symmetric, so   
(  
𝑢  
,  
𝑣  
)  
∈  
𝐴  
(u,v)∈A does not imply   
(  
𝑣  
,  
𝑢  
)  
∈  
𝐴  
(v,u)∈A, allowing for structures that capture oriented connections.\[20\]  
In a directed graph, the degree of a vertex splits into the in-degree and out-degree: the in-degree of vertex   
𝑣  
v is the number of arcs entering   
𝑣  
v, denoted   
deg  
⁡  
−  
(  
𝑣  
)  
deg   
−  
 (v), while the out-degree is the number of arcs leaving   
𝑣  
v, denoted   
deg  
⁡  
\+  
(  
𝑣  
)  
deg   
\+  
 (v).\[12\]\[23\] An extension of the handshaking lemma applies here: the sum of all in-degrees equals the sum of all out-degrees, and both equal the number of arcs   
∣  
𝐴  
∣  
∣A∣, since each arc contributes one to an in-degree and one to an out-degree.\[23\]\[24\]  
Prominent examples of directed graphs include tournaments and directed acyclic graphs (DAGs). A tournament is a directed graph on a vertex set   
𝑉  
V where, for every pair of distinct vertices   
𝑢  
,  
𝑣  
∈  
𝑉  
u,v∈V, exactly one of   
(  
𝑢  
,  
𝑣  
)  
(u,v) or   
(  
𝑣  
,  
𝑢  
)  
(v,u) is an arc, representing a complete orientation of the edges in a complete undirected graph.\[25\]\[26\] In contrast, a DAG is a directed graph containing no directed cycles, making it useful for modeling precedence relations, such as task scheduling where an arc   
(  
𝑢  
,  
𝑣  
)  
(u,v) indicates that task   
𝑢  
u must precede task   
𝑣  
v.\[27\]\[28\]  
Connectivity in directed graphs is assessed in two ways: strong and weak. A digraph is strongly connected if, for every pair of vertices   
𝑢  
,  
𝑣  
∈  
𝑉  
u,v∈V, there exists a directed path from   
𝑢  
u to   
𝑣  
v and from   
𝑣  
v to   
𝑢  
u.\[29\]\[30\] It is weakly connected if the underlying undirected graph—obtained by ignoring arc directions—is connected, allowing traversal between vertices regardless of direction.\[31\]\[32\]  
Any undirected graph can be converted to a directed graph through an orientation, which assigns a direction to each undirected edge, preserving the underlying structure while introducing asymmetry.\[33\]\[34\] This process is fundamental in studying properties like acyclicity or strong connectivity in oriented forms.\[35\]  
Graph Variants  
Graph variants extend the basic models of undirected and directed graphs by incorporating additional structures such as weights, multiple connections, or generalized edges to model more complex relationships.\[36\]  
Weighted graphs assign real numbers, known as weights, to the edges to represent quantities like distances, costs, or capacities in applications such as network routing. In a weighted graph, the adjacency matrix replaces binary entries with the corresponding edge weights, where the absence of an edge is typically denoted by zero or infinity depending on the context.\[36\] This structure facilitates algorithms for optimization problems, such as finding minimum-cost paths.  
Multigraphs generalize simple graphs by permitting multiple edges between the same pair of vertices, allowing representation of parallel connections in systems like transportation networks.\[36\] A pseudograph is a further extension that also allows loops, which are edges connecting a vertex to itself, useful for modeling self-referential relations.\[36\]  
Hypergraphs extend the edge concept beyond pairs of vertices, where each hyperedge connects an arbitrary subset of vertices, enabling the modeling of multi-way relationships such as in database dependencies or combinatorial designs.\[37\] Introduced formally in this framework, hypergraphs maintain the vertex set but replace pairwise edges with these generalized hyperedges.\[37\]  
Bipartite graphs partition the vertex set into two disjoint subsets such that no edge connects vertices within the same subset, with all edges crossing between the subsets; this structure arises in matching problems like assignment tasks.\[38\] A complete bipartite graph   
𝐾  
𝑚  
,  
𝑛  
K   
m,n  
​  
  connects every vertex in one subset of size   
𝑚  
m to every vertex in the other subset of size   
𝑛  
n, serving as a foundational example.\[38\]  
Trees are connected graphs with no cycles, providing a minimal structure for connectivity with exactly   
𝑛  
−  
1  
n−1 edges for   
𝑛  
n vertices, essential in hierarchical data representations like file systems.\[39\] Forests consist of disjoint unions of trees, representing collections of independent connected components without cycles.\[39\] The number of distinct labeled trees on   
𝑛  
n vertices is given by Cayley's formula   
𝑛  
𝑛  
−  
2  
n   
n−2  
 .\[39\]  
History  
Origins and Early Work  
The origins of graph theory trace back to the 18th century, with Leonhard Euler's seminal work on a practical problem in the city of Königsberg (now Kaliningrad, Russia). In 1736, Euler addressed the Seven Bridges of Königsberg problem, which asked whether it was possible to traverse all seven bridges connecting four landmasses exactly once and return to the starting point. He modeled the landmasses as vertices and the bridges as edges in a multigraph, introducing the concepts of traversability and what would later be termed Eulerian paths and circuits. Euler proved that no such closed tour exists because the graph has four vertices of odd degree, establishing the foundational insight that connectivity alone is insufficient for traversability.\[1\]  
Euler further defined an Eulerian circuit as a closed path that traverses each edge exactly once, occurring in a connected graph if and only if every vertex has even degree. An Eulerian path, which may start and end at different vertices, exists if exactly zero or two vertices have odd degree. These conditions, derived from parity arguments on edge incidences, marked the first systematic analysis of graph properties beyond mere connectivity and laid the groundwork for studying edge traversals. Euler's solution, published in the Commentarii Academiae Scientiarum Petropolitanae, is widely regarded as the birth of graph theory as a distinct mathematical discipline.\[1\]\[40\]  
In the 19th century, graph theory advanced through puzzle-based explorations and applications to counting and coloring. In 1847, Gustav Kirchhoff developed the matrix-tree theorem while studying electrical networks, providing a method to count the number of spanning trees in a connected graph by computing the determinant of a cofactor of its Laplacian matrix. This theorem equated the number of spanning trees to the value of any principal minor of the matrix formed by the degrees and adjacencies, bridging algebraic techniques with combinatorial enumeration. Meanwhile, in 1857, William Rowan Hamilton invented the Icosian game, a puzzle involving finding cycles that visit each vertex of a dodecahedral graph exactly once—now known as Hamiltonian cycles—popularizing the search for vertex-traversing tours distinct from Euler's edge-focused paths.\[1\]\[41\]  
Early applications extended to map coloring, with Francis Guthrie posing the four-color problem in 1852: whether any planar map could be colored using at most four colors such that adjacent regions receive different colors. This conjecture, communicated through Augustus De Morgan, translated to the chromatic number of planar graphs and spurred investigations by key figures like Peter Guthrie Tait, who in the 1880s attempted proofs by reducing it to edge-coloring cubic planar graphs, though his efforts revealed the problem's complexity without resolving it. These 19th-century contributions, centered on intuitive problems and manual verifications, emphasized graph theory's utility in geometry and puzzles before formal axiomatization.\[1\]\[42\]  
20th-Century Developments  
In the early 20th century, graph theory received a significant formalization through the works of Dénes Kőnig and Philip Hall on matchings in bipartite graphs. Kőnig's seminal book, Theorie der endlichen und unendlichen Graphen (1936), provided a comprehensive treatment of graph structures, including proofs of key results on bipartite matchings and vertex covers, establishing the equality between the size of a maximum matching and a minimum vertex cover in bipartite graphs. This built directly on Hall's earlier result, known as Hall's marriage theorem (1935), which states that in a bipartite graph with bipartition (X, Y), there exists a matching that covers all vertices in X if and only if for every subset S ⊆ X, the neighborhood N(S) satisfies |N(S)| ≥ |S|. These contributions formalized conditions for perfect matchings and laid foundational tools for combinatorial optimization. In 1930, Kazimierz Kuratowski characterized planar graphs, proving that a finite graph is planar if and only if it contains no subgraph homeomorphic to   
𝐾  
5  
K   
5  
​  
  or   
𝐾  
3  
,  
3  
K   
3,3  
​  
 .\[1\]  
A pivotal advancement in the mid-20th century was Ramsey's theorem (1930), which in its graph-theoretic form asserts that in any sufficiently large graph, or its complement, there exists a monochromatic clique of arbitrary size under edge colorings, guaranteeing the unavoidable emergence of ordered substructures in large systems. This theorem, initially motivated by logic, profoundly influenced graph theory by introducing ideas of unavoidable sets and sparking the field of Ramsey theory, which explores conditions for monochromatic subgraphs in colored graphs.  
Post-World War II, graph theory experienced explosive growth, particularly in extremal graph theory, driven by Paul Erdős and Pál Turán. Turán's theorem (1941) determines the maximum number of edges in an n-vertex graph without a complete subgraph K\_{r+1}, achieved uniquely by the balanced complete r-partite graph T(n, r), with edge count (1 \- 1/r) n^2 / 2\. Erdős extended this framework through numerous papers starting in the late 1940s, introducing probabilistic methods to bound extremal functions and proving results like the Erdős–Stone theorem (1946), which generalizes Turán's result to arbitrary forbidden subgraphs by relating extremal numbers to chromatic numbers. These developments shifted focus toward asymptotic bounds and structural extremal problems, establishing extremal graph theory as a core subdiscipline.  
The 1950s marked an algorithmic turn, exemplified by the Ford–Fulkerson algorithm and the max-flow min-cut theorem (1956), which prove that in a flow network, the maximum flow value equals the minimum cut capacity, enabling efficient computation of flows via augmenting paths.\[43\] By the 1960s, this algorithmic perspective permeated graph theory, integrating it with operations research and computer science, while combinatorial influences from Erdős and others fostered rapid institutional expansion. A major milestone came in 1976 with the proof of the four color theorem by Kenneth Appel and Wolfgang Haken, who used computer verification of reducible configurations to confirm that every planar graph is 4-colorable.\[1\]  
The field's maturation culminated in the founding of dedicated journals, such as the Journal of Graph Theory in 1977, which provided a platform for publishing advances in combinatorial graph structures and algorithms. This institutional growth reflected graph theory's evolution from isolated theorems to a vibrant branch of mathematics, deeply intertwined with broader combinatorics.  
Representations  
Adjacency Structures  
In graph theory, adjacency structures provide non-visual, computational representations that enable efficient storage, querying, and manipulation of graphs in algorithms and software implementations. These structures capture the connections between vertices without relying on geometric layouts, making them essential for processing large-scale graphs in fields like network analysis and optimization. Common variants include matrices and lists, each optimized for different graph densities and operations.  
The adjacency matrix is a square matrix   
𝐴  
A of size   
𝑛  
×  
𝑛  
n×n, where   
𝑛  
n is the number of vertices, and the entry   
𝐴  
𝑖  
𝑗  
A   
ij  
​  
  is 1 if there is an edge between vertices   
𝑖  
i and   
𝑗  
j, and 0 otherwise; for undirected graphs, the matrix is symmetric.\[44\] In directed graphs,   
𝐴  
𝑖  
𝑗  
\=  
1  
A   
ij  
​  
 \=1 indicates a directed edge from   
𝑖  
i to   
𝑗  
j, making the matrix potentially asymmetric.\[44\] For weighted graphs, entries store the weight of the edge instead of 1, allowing representation of edge costs or capacities.\[45\] This structure supports O(1) time for querying whether an edge exists between two vertices, though it requires   
Θ  
(  
𝑛  
2  
)  
Θ(n   
2  
 ) space regardless of the number of edges, which is inefficient for sparse graphs.\[46\]  
The adjacency list represents a graph as an array of lists, where each index corresponds to a vertex and the list at that index contains its neighboring vertices.\[47\] For undirected graphs, each edge appears in both endpoints' lists; in directed graphs, it appears only in the outgoing vertex's list. This structure achieves a space complexity of   
𝑂  
(  
∣  
𝑉  
∣  
\+  
∣  
𝐸  
∣  
)  
O(∣V∣+∣E∣), where   
∣  
𝑉  
∣  
∣V∣ is the number of vertices and   
∣  
𝐸  
∣  
∣E∣ is the number of edges, making it suitable for sparse graphs.\[46\] Traversing the neighbors of a vertex   
𝑣  
v takes   
𝑂  
(  
deg  
⁡  
(  
𝑣  
)  
)  
O(deg(v)) time, where   
deg  
⁡  
(  
𝑣  
)  
deg(v) is the degree of   
𝑣  
v, which is advantageous for algorithms like breadth-first search that iterate over adjacent vertices.\[47\]  
The incidence matrix is a   
∣  
𝑉  
∣  
×  
∣  
𝐸  
∣  
∣V∣×∣E∣ matrix   
𝐵  
B where rows correspond to vertices and columns to edges, with   
𝐵  
𝑣  
𝑒  
\=  
1  
B   
ve  
​  
 \=1 if vertex   
𝑣  
v is incident to edge   
𝑒  
e, and 0 otherwise; for directed graphs, it distinguishes incoming and outgoing edges with signs or separate entries.\[48\] This rectangular matrix is particularly useful in applications like network flows, where it models vertex-edge incidences for linear algebra-based computations such as solving flow conservation equations.\[48\] Its space complexity is   
𝑂  
(  
∣  
𝑉  
∣  
⋅  
∣  
𝐸  
∣  
)  
O(∣V∣⋅∣E∣), which can be higher than adjacency lists for dense graphs but facilitates operations involving all edges simultaneously.\[46\]  
An edge list is a simple collection of tuples or pairs, each specifying the endpoints of an edge, providing a compact representation without indexing by vertices.\[47\] It uses   
𝑂  
(  
∣  
𝐸  
∣  
)  
O(∣E∣) space, ideal for sparse graphs where vertex degrees are low, and supports easy iteration over all edges for algorithms like Kruskal's for minimum spanning trees.\[47\] However, checking for a specific edge requires linear time in   
∣  
𝐸  
∣  
∣E∣, limiting its use for frequent adjacency queries.\[47\]  
These adjacency structures complement visual graph drawings by enabling algorithmic efficiency in computational settings.\[47\]  
Visualizations  
Graph drawing methods aim to represent graphs in a visually intuitive manner, emphasizing structural properties such as connectivity and hierarchy. The most common approach uses node-link diagrams, in which vertices are positioned as points in the plane and edges are rendered as straight lines or curves connecting them, facilitating the perception of relationships and clusters within the graph.\[49\]  
For planar graphs, which admit embeddings without edge crossings, Fáry's theorem guarantees the existence of a straight-line drawing that preserves planarity, using only straight segments for edges without intersections. This result, proved in 1948, ensures that curved edges in planar embeddings can always be replaced by straight ones while maintaining the crossing-free property.\[50\]  
In non-planar graphs, edge crossings are inevitable, and the crossing number quantifies the minimum number of such crossings over all possible drawings. Computing the exact crossing number is NP-hard, even for restricted classes like cubic graphs, posing significant challenges for optimal layout algorithms.\[51\]  
Force-directed algorithms address layout challenges by modeling graphs as physical systems, particularly through spring embedders. Eades' 1984 algorithm treats vertices as repelling particles connected by attractive springs along edges, applying iterative forces—repulsive via an inverse-square law and attractive logarithmically—to converge on balanced, symmetric positions suitable for small graphs up to about 30 vertices.\[52\]  
For directed acyclic graphs (DAGs), layered or hierarchical drawings partition vertices into ordered horizontal layers based on topological levels, with edges directed downward to reveal precedence and flow. The Sugiyama framework, introduced in 1981, structures this process through cycle removal, layer assignment via longest paths, crossing minimization with barycenter heuristics, and coordinate refinement, producing clear visualizations of hierarchical structures like dependency networks.\[53\]  
Basic Structures and Operations  
Subgraphs and Minors  
In graph theory, a subgraph of a graph   
𝐺  
\=  
(  
𝑉  
,  
𝐸  
)  
G=(V,E) is a graph   
𝐻  
\=  
(  
𝑉  
′  
,  
𝐸  
′  
)  
H=(V   
′  
 ,E   
′  
 ) where   
𝑉  
′  
⊆  
𝑉  
V   
′  
 ⊆V and   
𝐸  
′  
⊆  
𝐸  
E   
′  
 ⊆E, with the edges in   
𝐸  
′  
E   
′  
  connecting vertices in   
𝑉  
′  
V   
′  
 .\[54\] This relation allows for the deletion of vertices and edges from   
𝐺  
G to form   
𝐻  
H, preserving the structural properties of the original graph where applicable.\[54\] A spanning subgraph of   
𝐺  
G retains all vertices in   
𝑉  
V but may delete some edges, resulting in a graph with vertex set   
𝑉  
V and a subset of   
𝐸  
E.\[55\]  
An induced subgraph, also known as a vertex-induced subgraph, arises from selecting a subset   
𝑆  
⊆  
𝑉  
S⊆V of vertices and including all edges from   
𝐸  
E that connect pairs of vertices in   
𝑆  
S; no edges are deleted between the chosen vertices.\[56\] This construction ensures that the subgraph captures the complete neighborhood relations among the selected vertices as they exist in   
𝐺  
G.\[56\] Induced subgraphs are crucial for studying hereditary properties, where the presence or absence of certain structures in subsets of vertices determines graph classes.\[56\]  
A graph minor provides a coarser structural relation than subgraphs. A graph   
𝐻  
H is a minor of   
𝐺  
G if   
𝐻  
H can be obtained from   
𝐺  
G by a sequence of vertex deletions, edge deletions, and edge contractions, where contracting an edge merges its endpoints into a single vertex and removes any resulting loops or multiple edges.\[57\] Edge contractions allow for the simplification of connected components, making minor containment a way to detect topological embeddings that are robust under local mergers.\[57\]  
The concept of minors underpins forbidden minor characterizations of graph families. Wagner's theorem states that a graph is planar if and only if it contains neither the complete graph   
𝐾  
5  
K   
5  
​  
  nor the complete bipartite graph   
𝐾  
3  
,  
3  
K   
3,3  
​  
  as a minor.\[57\] This result, from Wagner's 1937 work, refines earlier characterizations by emphasizing contractions alongside deletions.\[57\] Kuratowski's theorem complements this by characterizing non-planar graphs through forbidden subdivisions (topological minors) of   
𝐾  
5  
K   
5  
​  
  or   
𝐾  
3  
,  
3  
K   
3,3  
​  
 , where subdivisions replace edges with paths; for planarity, these are equivalent to the minor conditions in Wagner's formulation.\[57\]  
Graph isomorphism requires a bijective mapping between vertices that preserves adjacency exactly, meaning two graphs are identical up to relabeling. In contrast, minor containment is a weaker relation:   
𝐻  
H is a minor of   
𝐺  
G if   
𝐺  
G can be reduced to a graph isomorphic to   
𝐻  
H via deletions and contractions, allowing   
𝐺  
G to have additional structure beyond a mere copy of   
𝐻  
H.\[57\] Subgraph containment sits between them, requiring an isomorphic copy of   
𝐻  
H as a subgraph of   
𝐺  
G without contractions, but permitting extra vertices and edges in   
𝐺  
G.\[54\] These distinctions are fundamental in structural graph theory, where minors capture broad embeddability while isomorphisms demand precision.\[57\]  
Paths and Cycles  
In graph theory, a walk is a sequence of vertices and edges alternately connected, where vertices and edges may repeat, formally defined as a finite non-empty sequence   
𝑣  
0  
,  
𝑒  
1  
,  
𝑣  
1  
,  
…  
,  
𝑒  
𝑘  
,  
𝑣  
𝑘  
v   
0  
​  
 ,e   
1  
​  
 ,v   
1  
​  
 ,…,e   
k  
​  
 ,v   
k  
​  
  such that each edge   
𝑒  
𝑖  
e   
i  
​  
  is incident with vertices   
𝑣  
𝑖  
−  
1  
v   
i−1  
​  
  and   
𝑣  
𝑖  
v   
i  
​  
 . A trail is a walk with no repeated edges, and a path is a trail with no repeated vertices (except possibly the initial and terminal vertices coinciding). These structures form the basis for analyzing connectivity and traversals in graphs.  
A cycle is a closed path, meaning a path where the initial and terminal vertices are the same, with no other vertex repetitions, and at least three vertices. Paths and cycles induce subgraphs consisting of their vertices and edges, providing fundamental building blocks for more complex graph decompositions.  
A graph is connected if every pair of its vertices is joined by a path; otherwise, its connected components are the maximal connected subgraphs, partitioning the vertex set. An articulation point (or cut-vertex) is a vertex whose removal increases the number of connected components, while a bridge is an edge whose removal has the same effect. These elements identify critical points of vulnerability in graph connectivity.  
An Eulerian path (or trail) traverses each edge exactly once, existing in a connected graph if and only if exactly zero or two vertices have odd degree (the latter being the endpoints). An Eulerian circuit is a closed Eulerian path, requiring all vertices to have even degree in a connected graph; this characterization originates from Euler's solution to the Königsberg bridge problem.\[58\]  
A Hamiltonian path visits each vertex exactly once, and a Hamiltonian cycle is a closed such path; unlike Eulerian structures, no simple degree conditions suffice for their existence, and deciding whether a graph contains one is NP-complete.\[59\]  
Key Problems and Algorithms  
Connectivity and Flows  
In graph theory, the vertex connectivity of a graph   
𝐺  
G, denoted   
𝜅  
(  
𝐺  
)  
κ(G), is the minimum number of vertices whose removal disconnects   
𝐺  
G or reduces it to a single vertex, provided   
𝐺  
G is not complete.\[60\] Similarly, the edge connectivity   
𝜆  
(  
𝐺  
)  
λ(G) is the minimum number of edges whose removal disconnects   
𝐺  
G. These measures quantify the robustness of a graph against disconnection; for example, a graph is   
𝑘  
k-vertex-connected if   
𝜅  
(  
𝐺  
)  
≥  
𝑘  
κ(G)≥k, meaning at least   
𝑘  
k vertices must be removed to separate it. By convention, the connectivity of a complete graph   
𝐾  
𝑛  
K   
n  
​  
  is   
𝑛  
−  
1  
n−1, and isolated vertices have undefined connectivity.\[60\]  
Menger's theorem provides a path-based characterization of connectivity, stating that in an undirected graph, the minimum number of vertices separating two non-adjacent vertices   
𝑠  
s and   
𝑡  
t equals the maximum number of vertex-disjoint paths from   
𝑠  
s to   
𝑡  
t.\[61\] For edge connectivity, the edge version of Menger's theorem asserts that the minimum number of edges separating   
𝑠  
s and   
𝑡  
t equals the maximum number of edge-disjoint paths between them.\[61\] These theorems, proved by Karl Menger in 1927, link structural separation to path multiplicity and underpin many connectivity algorithms.\[61\]  
Network flows extend connectivity to capacitated directed graphs, where edges have non-negative capacities representing flow limits. A flow network includes a source vertex   
𝑠  
s and sink vertex   
𝑡  
t, with a feasible flow conserving flow at intermediate vertices and respecting capacities. The maximum flow problem seeks the highest total flow from   
𝑠  
s to   
𝑡  
t. The max-flow min-cut theorem, established by Ford and Fulkerson in 1956, equates this maximum flow value to the minimum capacity of an   
𝑠  
s-  
𝑡  
t cut—a partition of vertices into sets   
𝑆  
S (containing   
𝑠  
s) and   
𝑇  
T (containing   
𝑡  
t) where cut capacity is the sum of capacities of edges from   
𝑆  
S to   
𝑇  
T.\[43\]  
The Ford-Fulkerson algorithm computes maximum flow by iteratively finding augmenting paths in the residual graph—directed edges reflecting remaining capacity—and augmenting flow along them until no such path exists.\[43\] This method terminates for integer capacities but lacks polynomial time guarantees without specific path selection. The Edmonds-Karp variant, using breadth-first search for shortest augmenting paths, achieves   
𝑂  
(  
𝑉  
𝐸  
2  
)  
O(VE   
2  
 ) time complexity, where   
𝑉  
V is vertices and   
𝐸  
E is edges.\[62\] Dinic's algorithm improves efficiency by building a level graph via BFS and finding blocking flows in phases, yielding   
𝑂  
(  
𝑉  
2  
𝐸  
)  
O(V   
2  
 E) time.\[63\]  
Cuts formalize separation in flow networks: an   
𝑠  
s-  
𝑡  
t cut's capacity is the sum of forward capacities across the partition, and the min-cut equals the max-flow by the theorem.\[43\] Algorithms like Edmonds-Karp identify the min-cut as saturated edges in the final residual graph from the source side.\[62\]  
Maximum flows apply to bipartite matching by reducing the problem to a flow network: for bipartition   
𝑈  
U and   
𝑊  
W, add source edges of capacity 1 to   
𝑈  
U vertices and sink edges from   
𝑊  
W vertices, with unit capacities on original edges; the max-flow then equals the maximum matching size, as integer flows correspond to matchings.\[43\] This reduction, leveraging the integrality of flows, enables efficient computation of maximum cardinalities in bipartite graphs.\[62\]  
Coloring and Partitioning  
Graph coloring involves assigning colors to elements of a graph such that no two adjacent or incident elements receive the same color, serving as a fundamental tool for partitioning vertices or edges while respecting adjacency constraints. Vertex coloring specifically assigns colors to vertices so that adjacent vertices differ in color; the minimum number of colors required for such a proper coloring is the chromatic number, denoted   
𝜒  
(  
𝐺  
)  
χ(G).\[64\]\[65\] This concept underpins many partitioning strategies, as a k-coloring partitions the vertex set into k independent sets, with the chromatic number providing a lower bound on the size of such partitions. Determining   
𝜒  
(  
𝐺  
)  
χ(G) is NP-hard in general, but bounds and exact values exist for specific graph classes.\[65\]  
A seminal result bounding the chromatic number is Brooks' theorem, established in 1941\. For a connected graph   
𝐺  
G that is neither a complete graph nor an odd cycle,   
𝜒  
(  
𝐺  
)  
≤  
Δ  
(  
𝐺  
)  
χ(G)≤Δ(G), where   
Δ  
(  
𝐺  
)  
Δ(G) is the maximum degree of   
𝐺  
G.\[66\] This theorem implies that most graphs can be colored with no more colors than their maximum degree, offering a tight upper bound except for the specified exceptions, where   
𝜒  
(  
𝐺  
)  
\=  
Δ  
(  
𝐺  
)  
\+  
1  
χ(G)=Δ(G)+1. The proof relies on constructing a coloring by iteratively resolving conflicts in a greedy manner, highlighting the role of degree in limiting color requirements. Brooks' result has influenced subsequent work on coloring bounds and algorithmic approximations.\[66\]  
Edge coloring extends these ideas to edges, assigning colors so that no two edges incident to the same vertex share a color; the minimum number of colors needed is the chromatic index   
𝜒  
′  
(  
𝐺  
)  
χ   
′  
 (G). Vizing's theorem, proved in 1964, states that for any simple graph   
𝐺  
G,   
𝜒  
′  
(  
𝐺  
)  
χ   
′  
 (G) is either   
Δ  
(  
𝐺  
)  
Δ(G) or   
Δ  
(  
𝐺  
)  
\+  
1  
Δ(G)+1, classifying graphs as Class 1 or Class 2 accordingly.\[67\] The theorem's proof involves augmenting paths to resolve color conflicts, ensuring an edge coloring exists within the bound. This result is central to scheduling and resource allocation problems, where edges represent conflicts, and it remains a cornerstone for classifying edge-chromatic complexity.\[67\]  
Graph partitioning often leverages coloring for balanced divisions, such as equitable coloring, where a proper k-coloring has color classes differing in size by at most one. The Hajnal–Szemerédi theorem asserts that every graph with maximum degree   
Δ  
Δ admits an equitable k-coloring for any   
𝑘  
≥  
Δ  
\+  
1  
k≥Δ+1.\[68\] This guarantees balanced partitions into independent sets, with applications in load balancing and fair division; the bound is sharp, as complete graphs   
𝐾  
Δ  
\+  
1  
K   
Δ+1  
​  
  require   
Δ  
\+  
1  
Δ+1 colors and equitable classes of size 1\. Related partitioning problems, like minimum bisection—dividing vertices into two equal-sized sets while minimizing crossing edges—are NP-hard, even for planar graphs, underscoring the computational challenges beyond theoretical bounds.\[68\]  
A landmark achievement in vertex coloring is the four color theorem, proved in 1976 by Kenneth Appel and Wolfgang Haken using computer-assisted methods. It states that every planar graph   
𝐺  
G satisfies   
𝜒  
(  
𝐺  
)  
≤  
4  
χ(G)≤4, resolving a conjecture dating to 1852.\[69\] The proof reduces the problem to checking reducible configurations via discharging arguments, verifying over 1,900 cases computationally to ensure no counterexample exists. This theorem not only bounds coloring for planar graphs but also exemplifies the integration of theoretical combinatorics with computational verification, influencing map coloring and planar graph theory.\[69\]  
Enumeration and Optimization  
Graph enumeration involves counting the number of subgraphs isomorphic to a given pattern within a host graph, a problem central to combinatorial graph theory. While enumerating arbitrary subgraphs is computationally challenging and often \#P-complete, specific cases admit closed-form formulas. A seminal result is Cayley's formula, which states that the number of distinct spanning trees in the complete graph   
𝐾  
𝑛  
K   
n  
​  
  on   
𝑛  
n labeled vertices is exactly   
𝑛  
𝑛  
−  
2  
n   
n−2  
 .\[70\] This formula, proved using Prüfer codes or matrix-tree theorems, provides an exact count for tree subgraphs and has applications in network design and random graph analysis.\[71\]  
Optimization problems in graph theory seek to find substructures of minimal or maximal weight under constraints, often solvable via efficient algorithms for special cases. Shortest path problems compute the minimum-weight path between vertices in weighted graphs. Dijkstra's algorithm, applicable to graphs with non-negative edge weights, uses a priority queue to greedily expand from the source, achieving   
𝑂  
(  
(  
𝑉  
\+  
𝐸  
)  
log  
⁡  
𝑉  
)  
O((V+E)logV) time with a binary heap implementation.\[72\] For graphs permitting negative weights (but without negative cycles), the Bellman-Ford algorithm relaxes all edges   
∣  
𝑉  
∣  
−  
1  
∣V∣−1 times, detecting negative cycles if further relaxation is possible, and runs in   
𝑂  
(  
𝑉  
𝐸  
)  
O(VE) time.\[73\]  
Minimum spanning tree (MST) problems identify a tree of minimum total edge weight connecting all vertices in an undirected weighted graph. Kruskal's algorithm sorts edges by weight and adds them greedily if they connect disjoint components, using union-find for efficiency, yielding   
𝑂  
(  
𝐸  
log  
⁡  
𝐸  
)  
O(ElogE) time.\[74\] Prim's algorithm grows the MST from an arbitrary vertex by repeatedly selecting the minimum-weight edge connecting a tree vertex to an outside one, also achieving   
𝑂  
(  
𝐸  
log  
⁡  
𝑉  
)  
O(ElogV) time with suitable data structures.\[75\] Both algorithms guarantee an optimal MST via the cut property, ensuring greedy choices preserve optimality.\[76\]  
Matching problems aim to pair vertices via edges without sharing endpoints, maximizing size or weight. In bipartite graphs, maximum matchings can be found in   
𝑂  
(  
𝑉  
𝐸  
)  
O(   
V  
​  
 E) time using the Hopcroft-Karp algorithm, a refinement of the augmenting path method.\[77\] König's theorem establishes that in bipartite graphs, the size of the maximum matching equals the size of the minimum vertex cover, enabling duality-based optimizations. For general graphs, Edmonds' blossom algorithm computes maximum matchings in   
𝑂  
(  
𝑉  
4  
)  
O(V   
4  
 ) time by contracting odd cycles.  
The traveling salesman problem (TSP) requires finding a minimum-weight Hamiltonian cycle visiting all vertices exactly once. TSP is NP-hard, as shown by reduction from the Hamiltonian cycle problem.\[59\] For metric TSP (satisfying triangle inequality), Christofides' algorithm achieves a 1.5-approximation by combining an MST with a minimum-weight perfect matching on odd-degree vertices, then shortcutting to a tour. This remains the best known approximation ratio for general metric instances.  
Applications  
Computer Science and Networks  
In computer science, graph theory underpins key data structures used in software systems. Call graphs, which model function calls as directed edges between nodes representing procedures, are essential in compilers for tasks such as optimization, inlining, and dead code elimination.\[78\] These graphs enable analyses like interprocedural data flow, where vertices denote program points and edges capture control dependencies. In databases, graph representations facilitate query optimization by modeling join orders or execution plans as directed acyclic graphs (DAGs), allowing algorithms to select efficient evaluation strategies that minimize computational cost.\[79\]  
Fundamental graph traversal algorithms, such as breadth-first search (BFS) and depth-first search (DFS), form the basis for many computational tasks. BFS explores graphs level by level from a starting node, using a queue to ensure shortest-path discovery in unweighted graphs, with a time complexity of O(V \+ E) where V is vertices and E is edges. DFS, conversely, delves deeply along branches using a stack or recursion, enabling applications like cycle detection and topological ordering, also in O(V \+ E) time.\[80\] For directed acyclic graphs (DAGs), topological sort extends these traversals to linearize nodes respecting edge directions, as in Kahn's algorithm, which processes nodes with zero in-degree iteratively, achieving O(V \+ E) efficiency for scheduling dependencies in compilers or build systems.  
In network theory, graph algorithms optimize communication infrastructures. The Open Shortest Path First (OSPF) protocol, a link-state routing standard for IP networks, employs Dijkstra's algorithm on graph models of routers (nodes) and links (edges) to compute shortest-path trees, enabling dynamic route updates in response to topology changes.\[81\] Social network analysis leverages centrality measures to quantify node influence; betweenness centrality, for instance, assesses a vertex's control over information flow by counting shortest paths passing through it, with applications in identifying key influencers or bottlenecks.\[82\]  
Graph problems illuminate computational complexity boundaries. Many, like the Hamiltonian cycle—determining if a graph has a cycle visiting each vertex exactly once—are NP-complete, as proven by reduction from vertex cover, implying no known polynomial-time solution unless P \= NP. This hardness underscores the challenge in exact optimization for large graphs, driving heuristic and approximation approaches in practice.  
Recent advances integrate graphs with machine learning via Graph Neural Networks (GNNs), which propagate node features across edges to learn representations for tasks like node classification or link prediction. The Graph Convolutional Network (GCN), a seminal GNN variant, approximates spectral convolutions on graph Laplacians for semi-supervised learning, scaling to large datasets with O(V \+ E) per layer.\[83\]  
Physical and Biological Sciences  
In physics, graph theory provides a framework for modeling complex interactions, notably through Feynman diagrams, which represent particle interactions with vertices denoting interaction points and edges (lines) denoting particle propagators in quantum field theory calculations. Introduced by Richard Feynman in 1948, these diagrams simplify perturbative expansions by encoding mathematical amplitudes visually, enabling efficient computation of scattering processes in quantum electrodynamics. Percolation theory, another key application, uses random graphs to study phase transitions in disordered systems, such as the emergence of connected clusters in lattice graphs when edges are occupied with probability   
𝑝  
p. Pioneered by Broadbent and Hammersley in 1957, this model captures critical phenomena like fluid flow through porous media or conductivity thresholds, where a giant component forms at the percolation threshold   
𝑝  
𝑐  
p   
c  
​  
 , marking a transition from isolated clusters to long-range connectivity.\[84\]  
In chemistry, molecules are naturally modeled as undirected graphs, with vertices representing atoms and edges denoting chemical bonds, facilitating the analysis of structural properties and reactions. This representation, formalized in early graph-theoretic works on constitutional graphs, allows for the enumeration of isomers and prediction of molecular stability through topological indices like the Wiener index, which measures path lengths between atoms.\[85\] Graph isomorphism algorithms further enable the assessment of chemical similarity by determining if two molecular graphs share identical connectivity, crucial for database searching and drug design; for instance, subgraph isomorphism identifies common motifs in analogous compounds, supporting virtual screening in cheminformatics.\[86\]  
Biological systems leverage directed graphs to capture directional interactions, such as in metabolic pathways where vertices denote metabolites or enzymes and arcs represent biochemical reactions. These digraphs model flux directions and identify cycles in pathways like glycolysis, aiding in the discovery of regulatory bottlenecks through centrality measures.\[87\] Protein interaction networks, represented as undirected or weighted graphs with proteins as nodes and interactions as edges, reveal modular structures like complexes via community detection, with degree distributions often following power laws indicative of hubs essential for cellular function.\[88\] In ecology, food webs are modeled as bipartite graphs linking species (producers, consumers) via trophic edges, integrated with Lotka-Volterra equations to simulate predator-prey dynamics.  
Epidemiological models employ contact graphs to simulate disease spread, with the Susceptible-Infected-Recovered (SIR) framework propagating infections along edges in undirected networks. On scale-free graphs, characterized by hubs with high degrees, SIR dynamics exhibit no epidemic threshold, enabling rapid outbreaks even at low transmission rates, as observed in real-world pathogen transmissions.\[89\] Flow models on biological transport graphs, such as vascular networks, briefly reference max-flow algorithms to quantify nutrient distribution limits. Emerging applications include quantum graphs in quantum computing, where vertices host qubits and edges define entanglement or walks, enabling scalable simulation of quantum states via graph neural networks for optimization problems.\[90\]  
Social and Mathematical Contexts  
In social sciences, graph theory models interpersonal relationships, such as friendships, where individuals are represented as vertices and connections as edges, enabling analysis of network structures like centrality and clustering in social network analysis.\[91\] A prominent example is the small-world network model, introduced by Watts and Strogatz, which interpolates between regular lattices and random graphs to capture high clustering and short path lengths observed in real-world social connections, such as acquaintance networks.\[92\] Community detection algorithms, like the Louvain method developed by Blondel et al., optimize modularity to identify densely connected subgroups in large social graphs, revealing divisions such as interest-based clusters in online communities.\[93\]  
In linguistics, graph theory underpins syntactic analysis through dependency trees, where words form a tree structure with directed edges indicating head-dependent relations, facilitating parsing algorithms that project dependencies without crossing arcs for languages like English.\[94\] Semantic networks extend this by modeling lexical knowledge as graphs with nodes for concepts and labeled edges for relations like hypernymy or synonymy, supporting inference in natural language processing tasks such as word sense disambiguation.\[95\]  
Economic applications leverage graph theory in modeling strategic interactions over networks, particularly through graphical games where payoffs depend on local neighborhoods, allowing computation of Nash equilibria—stable strategy profiles where no player benefits from unilateral deviation—in settings like market competition or resource allocation.\[96\] Recent advancements in the 2020s apply graph neural networks to social media analytics, predicting user engagement by embedding interaction graphs with attention mechanisms to capture dynamic influences in platforms like Twitter.\[97\]  
In pure mathematics, Ramsey theory, originating from Ramsey's foundational work on order in large structures, guarantees that sufficiently large graphs contain monochromatic cliques or independent sets under edge colorings, with implications for combinatorics in avoiding disorder. Spectral graph theory examines the eigenvalues of the adjacency matrix to infer global properties, such as the largest eigenvalue bounding the maximum degree and connectivity via spectral gaps in expander graphs.\[98\] Algebraic graph theory integrates linear algebra and group theory to study graph invariants, like automorphism groups and spectrum, providing tools for isomorphism testing and expander constructions in combinatorial design.\[99\] Graph coloring briefly relates to social grouping by partitioning networks into independent sets representing non-adjacent communities.  
