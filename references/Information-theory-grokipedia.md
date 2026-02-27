# **Information theory**

Information theory is a mathematical discipline that quantifies, stores, and communicates information, focusing on the fundamental limits of data transmission and processing in the presence of [noise](https://grokipedia.com/page/Noise).\[1\] Founded by Claude E. Shannon through his seminal 1948 paper *"[A Mathematical Theory of Communication](https://grokipedia.com/page/A_Mathematical_Theory_of_Communication)"*, it treats information as a probabilistic entity, independent of its semantic meaning, and emphasizes engineering aspects of reliable message reproduction across communication systems.\[2\]\[1\]  
At its core, information theory introduces [entropy](https://grokipedia.com/page/Entropy) as the measure of uncertainty or average information content in a random source, defined for a discrete probability distribution as   
H=−∑pilog⁡2pi  
*H*\=−∑*p*  
*i*  
​  
log  
2  
​  
*p*  
*i*  
​  
 bits, where   
pi  
*p*  
*i*  
​  
 is the probability of each outcome.\[1\] This concept underpins source coding theorems, which establish that data can be compressed to a length approaching the source entropy without loss, enabling efficient storage and transmission.\[1\] Shannon's work also defines [channel capacity](https://grokipedia.com/page/Channel_capacity) as the supreme mutual information over all input distributions, representing the highest rate at which information can be sent reliably over a noisy channel, as formalized in his [noisy-channel coding theorem](https://grokipedia.com/page/Noisy-channel_coding_theorem).\[1\]\[2\]  
Key extensions include [mutual information](https://grokipedia.com/page/Mutual_information), which quantifies the shared information between two variables as   
I(X;Y)=H(X)+H(Y)−H(X,Y)  
*I*(*X*;*Y*)=*H*(*X*)+*H*(*Y*)−*H*(*X*,*Y*), essential for analyzing dependencies in communication and data processing.\[3\] The theory's impact spans [telecommunications](https://grokipedia.com/page/Telecommunications), where it optimizes signal encoding and error correction; [computing](https://grokipedia.com/page/Computing), influencing algorithms for compression and [cryptography](https://grokipedia.com/page/Cryptography); and broader fields like [biology](https://grokipedia.com/page/Biology), physics, and [machine learning](https://grokipedia.com/page/Machine_learning), where [entropy](https://grokipedia.com/page/Entropy) models uncertainty in genetic codes, thermodynamic systems, and neural networks.\[2\]\[1\] Shannon's binary digit (bit) as the unit of information laid the groundwork for the digital age, transforming [circuit design](https://grokipedia.com/page/Circuit_design) and enabling modern electronics.\[2\]

## **Introduction and History**

### **Overview**

Information theory is a branch of [applied mathematics](https://grokipedia.com/page/Applied_mathematics) and [electrical engineering](https://grokipedia.com/page/Electrical_engineering) primarily concerned with the quantification, storage, and communication of information.\[1\] It was pioneered by Claude E. Shannon in his seminal 1948 paper, which established a rigorous mathematical framework for analyzing information processes.\[1\] The field focuses on understanding how information can be measured in probabilistic terms, independent of its semantic meaning, to enable efficient handling in technical systems.\[4\]  
The core problems addressed by information theory include quantifying the [uncertainty](https://grokipedia.com/page/Uncertainty) inherent in messages or random events, devising efficient encoding techniques to minimize [redundancy](https://grokipedia.com/page/Redundancy) for storage and transmission, and designing methods to achieve reliable communication despite [noise](https://grokipedia.com/page/Noise) or interference in channels.\[1\] These challenges are foundational to modern digital systems, where resources like bandwidth and storage are limited. For instance, [information](https://grokipedia.com/page/Information) is conceptually viewed as the reduction of [uncertainty](https://grokipedia.com/page/Uncertainty): observing the outcome of a [fair coin](https://grokipedia.com/page/Fair_coin) flip eliminates one bit of uncertainty, whereas specifying a result from a fair six-sided die requires log₂(6) ≈ 2.58 bits on average.\[5\]  
Beyond its origins in engineering, information theory has exerted significant influence across interdisciplinary domains, including [computer science](https://grokipedia.com/page/Computer_science) for algorithm design, [biology](https://grokipedia.com/page/Biology) for modeling genetic information flows, and physics for connections to [thermodynamic entropy](https://grokipedia.com/page/Entropy).\[6\]\[7\] Central to the field is [entropy](https://grokipedia.com/page/Entropy) as a measure of uncertainty, with [channel capacity](https://grokipedia.com/page/Channel_capacity) defining the maximum rate of reliable transmission.\[1\]

### **Historical Development**

The origins of information theory trace back to early 20th-century efforts to quantify signal transmission in [telecommunications](https://grokipedia.com/page/Telecommunications). In 1924, [Harry Nyquist](https://grokipedia.com/page/Harry_Nyquist) published "Certain Factors Affecting Telegraph Speed" in the [Bell System](https://grokipedia.com/page/Bell_System) Technical Journal, where he derived a fundamental result establishing that a signal's maximum transmission rate is limited by twice the bandwidth, providing a foundational measure for the amount of information that could be sent over a channel without [distortion](https://grokipedia.com/page/Distortion), later contributing to the [sampling theorem](https://grokipedia.com/page/Theorem).\[8\] Building on this, Ralph Hartley introduced a quantitative measure of information in his 1928 paper "Transmission of Information" in the same journal, defining information as the logarithm of the number of possible distinguishable symbols, which laid the groundwork for logarithmic measures of uncertainty in communication systems.\[9\]  
The field crystallized with Claude Shannon's seminal 1948 paper "[A Mathematical Theory of Communication](https://grokipedia.com/page/A_Mathematical_Theory_of_Communication)," published in the [Bell System](https://grokipedia.com/page/Bell_System) Technical Journal, which formalized information theory by introducing concepts like [entropy](https://grokipedia.com/page/Entropy) as a measure of [uncertainty](https://grokipedia.com/page/Uncertainty) and [channel capacity](https://grokipedia.com/page/Channel_capacity) as the maximum reliable transmission rate over noisy channels, fundamentally shaping modern digital communication.\[1\] This work was popularized and extended beyond engineering to broader scientific audiences through Warren Weaver's collaboration in the 1949 book *The Mathematical Theory of Communication*, which emphasized the theory's implications for semantics and [human communication](https://grokipedia.com/page/Human_communication).\[10\]  
In the [1960s](https://grokipedia.com/page/1960s), information theory expanded into computational foundations with the development of [algorithmic information theory](https://grokipedia.com/page/Algorithmic_information_theory). Ray Solomonoff's 1960 technical report "A Preliminary Report on a General [Theory](https://grokipedia.com/page/Theory) of Inductive [Inference](https://grokipedia.com/page/Inference)" proposed measuring an object's [information content](https://grokipedia.com/page/Information_content) by the length of the shortest program that generates it, formalizing inductive inference through [algorithmic probability](https://grokipedia.com/page/Algorithmic_probability).\[11\] Independently, [Andrey Kolmogorov](https://grokipedia.com/page/Andrey_Kolmogorov) advanced this in his 1965 paper "Three Approaches to the Quantitative Definition of Information" in Problems of Information Transmission, and independently by [Gregory Chaitin](https://grokipedia.com/page/Gregory_Chaitin) in his 1966 paper "On the Length of Programs for Computing Finite Binary Sequences" in the Journal of the ACM, defining complexity as the minimal program length for computation, providing a non-probabilistic, algorithmic basis for information that influenced [computability](https://grokipedia.com/page/Computability) and [randomness](https://grokipedia.com/page/Randomness) studies.\[12\]\[13\]  
Quantum extensions emerged in the 1970s, with Alexander Holevo's 1973 paper "Bounds for the Quantity of Information Transmittable by a Quantum Communication Channel" in Problems of Information Transmission establishing the Holevo bound, which limits the classical information transmittable through quantum channels and founded quantum information theory.\[14\] By 2000, Michael Nielsen and Isaac Chuang's textbook [*Quantum Computation and Quantum Information*](https://grokipedia.com/page/Quantum_Computation_and_Quantum_Information) systematized quantum entropy and related measures, integrating classical information theory with [quantum mechanics](https://grokipedia.com/page/Quantum_mechanics) for applications in [quantum computing](https://grokipedia.com/page/Quantum_computing).\[15\]  
In the late [1990s](https://grokipedia.com/page/1990s) and [2000s](https://grokipedia.com/page/2000s), information theory intersected with [artificial intelligence](https://grokipedia.com/page/Artificial_intelligence), notably through Naftali Tishby's 1999 introduction of the information bottleneck method in the Proceedings of the 37th Allerton Conference, which optimizes data compression for relevant predictions by balancing information retention and compression, later applied to understand representation learning in neural networks.\[16\] This integration continued into the 2020s, with information-theoretic tools analyzing [deep learning](https://grokipedia.com/page/Deep_learning) dynamics, such as [mutual information](https://grokipedia.com/page/Mutual_information) flows in neural architectures, as explored in recent works unifying [Bayesian statistics](https://grokipedia.com/page/Bayesian_statistics) and Shannon entropy for [machine learning](https://grokipedia.com/page/Machine_learning) frameworks up to 2025\.\[17\]

## **Fundamental Quantities**

### **Entropy**

In information theory, entropy quantifies the average uncertainty or [information content](https://grokipedia.com/page/Information_content) associated with a discrete [random variable](https://grokipedia.com/page/Random_variable). For a discrete [random variable](https://grokipedia.com/page/Random_variable)   
X  
*X* taking values in a [finite set](https://grokipedia.com/page/Finite_set)   
X  
X with [probability mass function](https://grokipedia.com/page/Probability_mass_function)   
p(x)=Pr⁡(X=x)  
*p*(*x*)=Pr(*X*\=*x*) for   
x∈X  
*x*∈X, the [entropy](https://grokipedia.com/page/Entropy)   
H(X)  
*H*(*X*) is defined as

H(X)=−∑x∈Xp(x)log⁡2p(x),

*H*(*X*)=−

*x*∈X

∑

​

*p*(*x*)log

2

​

*p*(*x*),

where the logarithm is base 2, yielding a measure in bits. This formula, introduced by [Claude Shannon](https://grokipedia.com/page/Claude_Shannon), represents the [expected value](https://grokipedia.com/page/Expected_value) of the [information content](https://grokipedia.com/page/Information_content) of a single outcome, where the self-information of an event with probability   
p(x)  
*p*(*x*) is   
−log⁡2p(x)  
−log  
2  
​  
*p*(*x*), the number of bits needed to specify the outcome on average.  
Entropy serves as the fundamental limit on the average number of bits required to [encode](https://grokipedia.com/page/ENCODE) the outcomes of   
X  
*X* without loss of [information](https://grokipedia.com/page/Information), as established in lossless source coding theorems. For instance, consider a [fair coin](https://grokipedia.com/page/Fair_coin) flip, where   
X  
*X* is Bernoulli with   
p(0)=p(1)=1/2  
*p*(0)=*p*(1)=1/2; then   
H(X)=1  
*H*(*X*)=1 bit, indicating one bit suffices to describe the outcome on average. For a biased coin with   
p(1)=0.9  
*p*(1)=0.9 and   
p(0)=0.1  
*p*(0)=0.1,   
H(X)=−0.9log⁡20.9−0.1log⁡20.1≈0.469  
*H*(*X*)=−0.9log  
2  
​  
0.9−0.1log  
2  
​  
0.1≈0.469 bits, reflecting lower [uncertainty](https://grokipedia.com/page/Uncertainty) due to the bias.  
The [binary entropy function](https://grokipedia.com/page/Binary_entropy_function)   
h(p)  
*h*(*p*), a special case for Bernoulli random variables with success probability   
p  
*p*, is given by

h(p)=−plog⁡2p−(1−p)log⁡2(1−p),

*h*(*p*)=−*p*log

2

​

*p*−(1−*p*)log

2

​

(1−*p*),

which reaches its maximum of 1 bit at   
p=0.5  
*p*\=0.5 and approaches 0 as   
p  
*p* nears 0 or 1\. More generally, [entropy](https://grokipedia.com/page/Entropy) can be expressed in other units: nats using the natural logarithm (dividing by   
ln⁡2  
ln2 converts bits to nats) or hartleys using base-10 logarithm, though bits are standard in digital contexts for aligning with binary encoding.  
Key properties of entropy include non-negativity,   
H(X)≥0  
*H*(*X*)≥0, with equality if and only if   
X  
*X* is deterministic (one outcome has probability 1); this follows from [Jensen's inequality](https://grokipedia.com/page/Jensen's_inequality) applied to the [concave function](https://grokipedia.com/page/Concave_function)   
−log⁡2p  
−log  
2  
​  
*p*. Entropy is maximized for the uniform distribution over   
X  
X, where   
H(X)=log⁡2∣X∣  
*H*(*X*)=log  
2  
​  
∣X∣, providing an upper bound on [uncertainty](https://grokipedia.com/page/Uncertainty) for a given alphabet size. For independent random variables   
X  
*X* and   
Y  
*Y*, entropy is additive:   
H(X,Y)=H(X)+H(Y)  
*H*(*X*,*Y*)=*H*(*X*)+*H*(*Y*).  
Shannon derived the entropy function from a set of axioms in his seminal 1948 paper: the measure must be continuous in the probabilities, monotonically increasing as probabilities become more uniform, uniquely determined up to a constant multiplier, and additive for independent events. Solving these yields   
H(X)=−K∑p(x)log⁡p(x)  
*H*(*X*)=−*K*∑*p*(*x*)log*p*(*x*) for some positive constant   
K  
*K*, with   
K=1/ln⁡2  
*K*\=1/ln2 chosen for bits; the proof involves showing that the logarithmic form satisfies the axioms and is unique.

### **Joint and Conditional Entropy**

Joint entropy extends the concept of [entropy](https://grokipedia.com/page/Entropy) to two or more random variables, quantifying the total uncertainty in their joint occurrence. For discrete random variables   
X  
*X* and   
Y  
*Y* with joint probability mass function   
p(x,y)  
*p*(*x*,*y*), the joint entropy   
H(X,Y)  
*H*(*X*,*Y*) is defined as

H(X,Y)=−∑x,yp(x,y)log⁡2p(x,y),

*H*(*X*,*Y*)=−

*x*,*y*

∑

​

*p*(*x*,*y*)log

2

​

*p*(*x*,*y*),

which represents the average number of bits needed to specify both   
X  
*X* and   
Y  
*Y* together.\[1\] This measure averages the self-information over the joint distribution, capturing dependencies between the variables.\[18\]  
A key property of joint entropy is its [subadditivity](https://grokipedia.com/page/Subadditivity):   
H(X,Y)≤H(X)+H(Y)  
*H*(*X*,*Y*)≤*H*(*X*)+*H*(*Y*), with equality holding if and only if   
X  
*X* and   
Y  
*Y* are independent.\[18\] Additionally,   
H(X,Y)≥max⁡(H(X),H(Y))  
*H*(*X*,*Y*)≥max(*H*(*X*),*H*(*Y*)), reflecting that the combined [uncertainty](https://grokipedia.com/page/Uncertainty) cannot be less than the uncertainty of either variable alone.\[18\] The chain rule provides a decomposition:   
H(X,Y)=H(X)+H(Y∣X)  
*H*(*X*,*Y*)=*H*(*X*)+*H*(*Y*∣*X*), linking joint entropy to [conditional entropy](https://grokipedia.com/page/Conditional_entropy) and enabling recursive extensions to more variables, such as   
H(X1,…,Xn)=∑i=1nH(Xi∣X1,…,Xi−1)  
*H*(*X*  
1  
​  
,…,*X*  
*n*  
​  
)=∑  
*i*\=1  
*n*  
​  
*H*(*X*  
*i*  
​  
∣*X*  
1  
​  
,…,*X*  
*i*−1  
​  
).\[1\]  
Conditional entropy   
H(Y∣X)  
*H*(*Y*∣*X*) measures the average remaining uncertainty about   
Y  
*Y* after observing   
X  
*X*. It is formally defined as

H(Y∣X)=−∑x,yp(x,y)log⁡2p(y∣x)=H(X,Y)−H(X),

*H*(*Y*∣*X*)=−

*x*,*y*

∑

​

*p*(*x*,*y*)log

2

​

*p*(*y*∣*x*)=*H*(*X*,*Y*)−*H*(*X*),

where   
p(y∣x)=p(x,y)/p(x)  
*p*(*y*∣*x*)=*p*(*x*,*y*)/*p*(*x*) is the [conditional probability](https://grokipedia.com/page/Conditional_probability) mass function.\[1\] This quantity interprets as the expected [entropy](https://grokipedia.com/page/Entropy) of   
Y  
*Y* given each possible value of   
X  
*X*, weighted by the probability of   
X  
*X*.\[18\]  
Properties of conditional entropy include non-negativity:   
H(Y∣X)≥0  
*H*(*Y*∣*X*)≥0, with equality if   
Y  
*Y* is a deterministic function of   
X  
*X*.\[18\] Furthermore, conditioning cannot increase [entropy](https://grokipedia.com/page/Entropy):   
H(Y∣X)≤H(Y)  
*H*(*Y*∣*X*)≤*H*(*Y*), with equality if   
X  
*X* and   
Y  
*Y* are independent, indicating that knowledge of   
X  
*X* either reduces or leaves unchanged the [uncertainty](https://grokipedia.com/page/Uncertainty) in   
Y  
*Y*.\[1\]  
As an example, consider two fair coin flips   
X  
*X* and   
Y  
*Y*. If independent, the joint entropy   
H(X,Y)=2  
*H*(*X*,*Y*)=2 bits, equal to   
H(X)+H(Y)=1+1  
*H*(*X*)+*H*(*Y*)=1+1.\[18\] If   
Y=X  
*Y*\=*X* (perfect dependence), then   
H(X,Y)=1  
*H*(*X*,*Y*)=1 bit, which is   
max⁡(H(X),H(Y))  
max(*H*(*X*),*H*(*Y*)). For conditional entropy, suppose   
Y  
*Y* is the next English letter after observing   
X  
*X* as the previous letter;   
H(Y∣X)  
*H*(*Y*∣*X*) is about 1.3 bits, much less than the unconditional   
H(Y)≈4.1  
*H*(*Y*)≈4.1 bits, due to contextual dependencies.\[1\]

### **Mutual Information**

Mutual information quantifies the amount of information that one [random variable](https://grokipedia.com/page/Random_variable) contains about another, serving as a measure of their statistical dependence.\[1\] Introduced by [Claude Shannon](https://grokipedia.com/page/Claude_Shannon) in his foundational work on [communication theory](https://grokipedia.com/page/Communication_theory), it captures the shared [uncertainty](https://grokipedia.com/page/Uncertainty) between two variables without assuming a specific form of relationship, such as [linearity](https://grokipedia.com/page/Linearity).\[1\]  
Formally, for discrete random variables   
X  
*X* and   
Y  
*Y* with joint [probability mass function](https://grokipedia.com/page/Probability_mass_function)   
p(x,y)  
*p*(*x*,*y*), the [mutual information](https://grokipedia.com/page/Mutual_information)   
I(X;Y)  
*I*(*X*;*Y*) is defined as the difference between the [entropy](https://grokipedia.com/page/Entropy) of   
X  
*X* and the [conditional entropy](https://grokipedia.com/page/Conditional_entropy) of   
X  
*X* given   
Y  
*Y*:

I(X;Y)=H(X)−H(X∣Y).

*I*(*X*;*Y*)=*H*(*X*)−*H*(*X*∣*Y*).

This equals the Kullback-Leibler divergence between the joint distribution and the product of the marginals:

I(X;Y)=∑x∑yp(x,y)log⁡p(x,y)p(x)p(y),

*I*(*X*;*Y*)=

*x*

∑

​

*y*

∑

​

*p*(*x*,*y*)log

*p*(*x*)*p*(*y*)

*p*(*x*,*y*)

​

,

where the logarithm is base 2 for units in bits.\[1\] The measure is symmetric, such that   
I(X;Y)=I(Y;X)  
*I*(*X*;*Y*)=*I*(*Y*;*X*), reflecting that the information   
Y  
*Y* provides about   
X  
*X* is the same as the information   
X  
*X* provides about   
Y  
*Y*.\[1\]  
Mutual information possesses several key properties. It is non-negative,   
I(X;Y)≥0  
*I*(*X*;*Y*)≥0, with equality holding if and only if   
X  
*X* and   
Y  
*Y* are independent, meaning knowledge of one provides no [information](https://grokipedia.com/page/Information) about the other.\[1\] Additionally, it is bounded above by the minimum of the individual [entropies](https://grokipedia.com/page/Entropy):   
I(X;Y)≤min⁡(H(X),H(Y))  
*I*(*X*;*Y*)≤min(*H*(*X*),*H*(*Y*)), ensuring it cannot exceed the inherent uncertainty in either variable.\[1\]  
In interpretive terms, mutual information represents the average reduction in uncertainty about   
X  
*X* upon observing   
Y  
*Y*, or equivalently, the number of bits of information shared between the two variables.\[1\] This makes it a fundamental tool for assessing dependence in probabilistic systems, distinct from joint and [conditional entropy](https://grokipedia.com/page/Conditional_entropy), which measure absolute or context-dependent uncertainties.\[1\]  
A chain rule extends mutual information to multiple variables: for random variables   
X1,X2,…,Xn  
*X*  
1  
​  
,*X*  
2  
​  
,…,*X*  
*n*  
​  
 and   
Y  
*Y*,

I(X1,X2,…,Xn;Y)=I(X1;Y)+I(X2;Y∣X1)+⋯+I(Xn;Y∣X1,…,Xn−1),

*I*(*X*

1

​

,*X*

2

​

,…,*X*

*n*

​

;*Y*)=*I*(*X*

1

​

;*Y*)+*I*(*X*

2

​

;*Y*∣*X*

1

​

)+⋯+*I*(*X*

*n*

​

;*Y*∣*X*

1

​

,…,*X*

*n*−1

​

),

allowing decomposition of total dependence into conditional contributions.\[19\]  
Examples illustrate these concepts clearly. If   
X  
*X* and   
Y  
*Y* are independent, then   
p(x,y)=p(x)p(y)  
*p*(*x*,*y*)=*p*(*x*)*p*(*y*), so   
I(X;Y)=0  
*I*(*X*;*Y*)=0.\[1\] Conversely, if   
Y=X  
*Y*\=*X* (identical variables), then   
H(X∣Y)=0  
*H*(*X*∣*Y*)=0, yielding   
I(X;Y)=H(X)  
*I*(*X*;*Y*)=*H*(*X*), the full entropy of   
X  
*X*.\[1\]

### **Divergence Measures**

Divergence measures in information theory quantify the difference between two probability distributions, with the Kullback-Leibler (KL) divergence serving as a foundational example. For discrete probability distributions   
P  
*P* and   
Q  
*Q* over the same [sample space](https://grokipedia.com/page/Sample_space), the KL divergence is defined as

KL(P∥Q)=∑xP(x)log⁡P(x)Q(x),

KL(*P*∥*Q*)=

*x*

∑

​

*P*(*x*)log

*Q*(*x*)

*P*(*x*)

​

,

where the logarithm is typically base-2 for bits or natural for nats.\[20\] This measure is always non-negative,   
KL(P∥Q)≥0  
KL(*P*∥*Q*)≥0, and equals zero if and only if   
P=Q  
*P*\=*Q* [almost everywhere](https://grokipedia.com/page/Almost_everywhere), a property established via the [Gibbs inequality](https://grokipedia.com/page/Gibbs'_inequality). For continuous distributions, the sum is replaced by an [integral](https://grokipedia.com/page/Integral):   
KL(P∥Q)=∫p(x)log⁡p(x)q(x) dx  
KL(*P*∥*Q*)=∫*p*(*x*)log  
*q*(*x*)  
*p*(*x*)  
​  
*dx*.\[20\]  
The KL divergence exhibits key properties that distinguish it from metric distances. It is asymmetric, meaning   
KL(P∥Q)≠KL(Q∥P)  
KL(*P*∥*Q*)  
\=KL(*Q*∥*P*) in general, reflecting its directed nature from   
P  
*P* to   
Q  
*Q*. Additionally, it does not satisfy the [triangle inequality](https://grokipedia.com/page/Triangle_inequality), preventing it from forming a true [distance](https://grokipedia.com/page/Distance) metric on the space of probability distributions. Introduced by Solomon Kullback and Richard Leibler in 1951, the KL divergence originated in the context of statistical hypothesis testing and information sufficiency.\[20\]  
Interpretationally,   
KL(P∥Q)  
KL(*P*∥*Q*) represents the expected number of extra bits required to encode samples drawn from   
P  
*P* using a code optimized for   
Q  
*Q*, rather than one optimal for   
P  
*P*. Equivalently, it measures the information gain obtained when using the true distribution   
P  
*P* instead of the approximation   
Q  
*Q*. This connects to [mutual information](https://grokipedia.com/page/Mutual_information), where   
I(X;Y)=EY\[KL(PX∣Y∥PX)\]  
*I*(*X*;*Y*)=E  
*Y*  
​  
\[KL(*P*  
*X*∣*Y*  
​  
∥*P*  
*X*  
​  
)\], quantifying the average divergence between the conditional and marginal distributions of   
X  
*X*.  
A concrete example arises with Bernoulli distributions, where   
P∼Bern(p)  
*P*∼Bern(*p*) and   
Q∼Bern(q)  
*Q*∼Bern(*q*). The KL divergence simplifies to   
KL(P∥Q)=plog⁡pq+(1−p)log⁡1−p1−q  
KL(*P*∥*Q*)=*p*log  
*q*  
*p*  
​  
\+(1−*p*)log  
1−*q*  
1−*p*  
​  
, illustrating how it penalizes mismatches in success probabilities; for instance, with   
p=0.5  
*p*\=0.5 and   
q=0.6  
*q*\=0.6,   
KL(P∥Q)≈0.029  
KL(*P*∥*Q*)≈0.029 bits. In applications like [model selection](https://grokipedia.com/page/Model_selection), the KL divergence underpins criteria such as the [Akaike Information Criterion](https://grokipedia.com/page/Akaike_information_criterion) (AIC), which estimates the expected relative [entropy](https://grokipedia.com/page/Entropy) between the true data-generating [process](https://grokipedia.com/page/Process) and a fitted model to balance goodness-of-fit and complexity.\[21\]

## **Source Coding**

### **Compression Fundamentals**

Source coding theory addresses the compression of data from information sources without loss of information, establishing fundamental limits on achievable compression rates. The source coding theorem, also known as the noiseless coding theorem, states that for a discrete memoryless source producing symbols from alphabet   
X  
X with probability distribution   
p(x)  
*p*(*x*), the optimal average codeword length   
L  
*L* for any uniquely decodable code satisfies   
L≥H(X)  
*L*≥*H*(*X*), where   
H(X)=−∑x∈Xp(x)log⁡2p(x)  
*H*(*X*)=−∑  
*x*∈X  
​  
*p*(*x*)log  
2  
​  
*p*(*x*) is the entropy of the source.\[1\] This bound is achievable in the limit as the block length increases, meaning sequences of source symbols can be compressed to rates arbitrarily close to the entropy using block codes that are uniquely decodable.\[1\]  
The theorem implies that the minimum compression rate   
R  
*R* required for reliable lossless encoding of the source is   
R≥H(X)  
*R*≥*H*(*X*) bits per symbol, ensuring that the encoded representation captures the inherent uncertainty or [information content](https://grokipedia.com/page/Information_content) of the source without redundancy beyond this limit.\[1\] For sources with [entropy](https://grokipedia.com/page/Entropy) lower than the logarithm of the [alphabet](https://grokipedia.com/page/Alphabet) size, significant compression is possible by exploiting statistical dependencies, as [entropy](https://grokipedia.com/page/Entropy) quantifies the average surprise or unpredictability per symbol.  
Huffman coding provides an optimal prefix-free code for discrete memoryless sources with known symbol probabilities, achieving an average code length within 1 bit of the [entropy](https://grokipedia.com/page/Entropy) bound.\[22\] The algorithm proceeds by first sorting the symbols in decreasing order of their probabilities. It then iteratively builds a [binary tree](https://grokipedia.com/page/Binary_tree): the two symbols (or subtrees) with the lowest probabilities are combined into a new node with probability equal to their sum, assigning 0 and 1 to the branches, and this process repeats until a single root remains. The codewords are the paths from root to leaves, ensuring no code is a prefix of another and minimizing the weighted path length, which equals the average code length.\[22\]  
Arithmetic coding offers superior efficiency for memoryless sources by encoding entire messages as fractions of the unit interval, rather than fixed-length codes per [symbol](https://grokipedia.com/page/Symbol), approaching the [entropy](https://grokipedia.com/page/Entropy) bound more closely without the integer-length overhead of [block codes](https://grokipedia.com/page/Block_code).\[23\] In this method, the message's probability interval   
\[0,1)  
\[0,1) is subdivided according to symbol probabilities; each symbol narrows the current interval proportionally, and the final interval's binary representation (or a tag within it) serves as the code, with the decoder reversing the process to recover the symbols. This fractional encoding allows the code length to be approximately   
−log⁡2P(m)  
−log  
2  
​  
*P*(*m*) bits for message   
m  
*m* with probability   
P(m)  
*P*(*m*), yielding near-entropy performance even for single symbols.\[23\]  
A practical example is the compression of English text, where the entropy is approximately 1 to 1.5 bits per character due to letter frequencies and contextual redundancies in [natural language](https://grokipedia.com/page/Natural_language), far below the 4.7 bits per character (log₂26 for lowercase letters) of uniform encoding.\[24\] This redundancy, arising from predictable patterns like common digrams and grammatical structure, enables compression ratios of about 3:1 to 5:1 using entropy-based methods, as demonstrated in early human prediction experiments that estimated the per-character information content.\[24\]

### **Practical Coding Techniques**

Variable-length codes assign shorter codewords to more probable symbols and longer ones to less probable symbols, enabling efficient compression of sources with uneven symbol probabilities. One early method is Shannon-Fano coding, which constructs codes by recursively splitting the [alphabet](https://grokipedia.com/page/Alphabet) into two subsets of approximately equal total probability, assigning binary digits accordingly.\[1\]\[25\] This top-down approach ensures the code lengths are close to the negative logarithm of the probabilities, though it may not always yield optimal lengths.\[1\]  
In contrast, Huffman coding achieves optimality for prefix-free codes over a fixed [alphabet](https://grokipedia.com/page/Alphabet) by building a [binary tree](https://grokipedia.com/page/Binary_tree) bottom-up, merging the two least probable symbols iteratively to form [code](https://grokipedia.com/page/Code)words whose lengths satisfy the Kraft inequality with equality.\[22\] While Shannon-Fano is simpler to implement without requiring full probability sorting, Huffman codes generally produce shorter average lengths, making them preferable for static sources where the full [alphabet](https://grokipedia.com/page/Alphabet) is known in advance.\[22\] Both methods approach the entropy bound for large alphabets but incur redundancy for small ones due to [integer](https://grokipedia.com/page/Integer) code lengths.  
For universal compression of unknown or streaming data, the Lempel-Ziv-Welch (LZW) algorithm builds a dictionary adaptively by replacing repeated substrings with codes referencing prior occurrences.\[26\] Starting from an initial dictionary of single symbols, LZW parses the input into phrases, outputs the code for the longest matching prefix, and adds the extension to the dictionary, enabling real-time learning without prior statistics.\[27\] This variant of the LZ78 scheme excels on repetitive data, achieving compression ratios near the [entropy rate](https://grokipedia.com/page/Entropy_rate) asymptotically, and is widely used in formats like ZIP archives and [GIF](https://grokipedia.com/page/GIF) images for its simplicity and effectiveness on text and graphics.\[26\]  
Lossy compression techniques sacrifice fidelity for higher rates, guided by rate-distortion theory, which quantifies the minimum rate   
R(D)  
*R*(*D*) needed to represent a source at average distortion no greater than   
D  
*D*. For a source   
X  
*X* and reproduction   
X^  
*X*  
^  
 with distortion   
E\[d(X,X^)\]≤D  
*E*\[*d*(*X*,  
*X*  
^  
)\]≤*D*,

R(D)=min⁡p(x^∣x):E\[d(X,X^)\]≤DI(X;X^),

*R*(*D*)=

*p*(

*x*

^

∣*x*):*E*\[*d*(*X*,

*X*

^

)\]≤*D*

min

​

*I*(*X*;

*X*

^

),

where the [mutual information](https://grokipedia.com/page/Mutual_information)   
I(X;X^)  
*I*(*X*;  
*X*  
^  
) captures the information preserved in the approximation.\[1\] Practical source-side methods focus on transforming the [data](https://grokipedia.com/page/Data) to concentrate [energy](https://grokipedia.com/page/Energy) in few coefficients, quantizing them coarsely for low distortion, and [entropy](https://grokipedia.com/page/Entropy)\-coding the result, balancing rate against perceptual quality without channel considerations.  
Adaptive coding addresses non-stationary sources by updating models on-the-fly, avoiding assumptions of fixed statistics. Prediction by partial matching (PPM) exemplifies this by estimating symbol probabilities based on increasingly longer contexts from recent history, escaping to lower-order models when unseen patterns arise to prevent [overfitting](https://grokipedia.com/page/Overfitting).\[28\] This hierarchical approach achieves superior compression on [natural language](https://grokipedia.com/page/Natural_language) or [code](https://grokipedia.com/page/Code) by capturing evolving dependencies, often outperforming static Huffman on adaptive arithmetic coders.  
A representative application is the [JPEG](https://grokipedia.com/page/JPEG) standard for [image compression](https://grokipedia.com/page/Image_compression), which applies the [discrete cosine transform](https://grokipedia.com/page/Discrete_cosine_transform) (DCT) to 8x8 blocks to decorrelate pixels based on spatial statistics, yielding coefficients that are quantized and Huffman-coded.\[29\] By exploiting human visual sensitivity—retaining low-frequency details while discarding high-frequency [noise](https://grokipedia.com/page/Noise)—JPEG trades minor artifacts for ratios of 10:1 to 20:1 on typical photos, though computational costs in DCT and quantization rise with [image resolution](https://grokipedia.com/page/Image_resolution). These techniques highlight the tension between achieving near-theoretical rates and practical constraints like decoder simplicity.

## **Channel Coding**

### **Capacity and Noisy Channels**

In information theory, a discrete memoryless channel (DMC) is modeled as a probabilistic mapping from input symbols   
X  
*X* drawn from a finite [alphabet](https://grokipedia.com/page/Alphabet)   
X  
X to output symbols   
Y  
*Y* from a finite [alphabet](https://grokipedia.com/page/Alphabet)   
Y  
Y, characterized by conditional transition probabilities   
p(y∣x)  
*p*(*y*∣*x*) that specify the probability of receiving   
y  
*y* given that   
x  
*x* was transmitted, with outputs independent across time slots.\[1\]  
The capacity   
C  
*C* of such a channel represents the supremum of rates at which information can be reliably transmitted and is defined as the maximum mutual information between input and output over all possible input distributions:

C=max⁡p(x)I(X;Y),

*C*\=

*p*(*x*)

max

​

*I*(*X*;*Y*),

where   
I(X;Y)=H(Y)−H(Y∣X)  
*I*(*X*;*Y*)=*H*(*Y*)−*H*(*Y*∣*X*) quantifies the reduction in uncertainty about   
Y  
*Y* provided by knowledge of   
X  
*X*.\[1\]  
Shannon's noisy-channel coding theorem establishes the fundamental limits of reliable communication over such channels: for any rate   
R\<C  
*R*\<*C*, there exists a coding scheme achieving arbitrarily low probability of error as the block length   
n→∞  
*n*→∞; conversely, for   
R\>C  
*R*\>*C*, the error probability is bounded away from zero.\[1\]  
A sketch of the achievability proof relies on random coding and typical set decoding. In random coding,   
2nR  
2  
*nR*  
 codewords are generated independently for each message, with each symbol drawn i.i.d. from the capacity-achieving input distribution   
p(x)  
*p*(*x*); the average error probability over this ensemble vanishes exponentially as   
n→∞  
*n*→∞ for   
R\<I(X;Y)  
*R*\<*I*(*X*;*Y*), implying the existence of at least one good code via the [probabilistic method](https://grokipedia.com/page/Probabilistic_method). For decoding, the receiver selects the unique codeword jointly typical with the received sequence   
yn  
*y*  
*n*  
, where jointly typical sequences   
(xn,yn)  
(*x*  
*n*  
,*y*  
*n*  
) satisfy   
∣p^(xi,yi)−p(xi,yi)∣\<ϵ/n  
∣  
*p*  
^  
​  
(*x*  
*i*  
​  
,*y*  
*i*  
​  
)−*p*(*x*  
*i*  
​  
,*y*  
*i*  
​  
)∣\<*ϵ*/*n* for small   
ϵ  
*ϵ*, ensuring that with high probability, the correct codeword is decoded due to the concentration of probability mass on the [typical set](https://grokipedia.com/page/Typical_set) of size approximately   
2nH(X,Y)  
2  
*nH*(*X*,*Y*)  
.\[30\]  
For the binary symmetric channel (BSC), where   
X=Y={0,1}  
X=Y={0,1} and bits flip with probability   
p\<1/2  
*p*\<1/2, the capacity-achieving input distribution is [uniform](https://grokipedia.com/page/Uniform), yielding

C=1−h2(p),

*C*\=1−*h*

2

​

(*p*),

with   
h2(p)=−plog⁡2p−(1−p)log⁡2(1−p)  
*h*  
2  
​  
(*p*)=−*p*log  
2  
​  
*p*−(1−*p*)log  
2  
​  
(1−*p*) the [binary entropy function](https://grokipedia.com/page/Binary_entropy_function), so   
C=1  
*C*\=1 bit per use when   
p=0  
*p*\=0 (noiseless) and decreases to 0 as   
p→1/2  
*p*→1/2.\[1\]  
In the continuous-time setting with [additive white Gaussian noise](https://grokipedia.com/page/Additive_white_Gaussian_noise) (AWGN), the channel adds independent [Gaussian noise](https://grokipedia.com/page/Gaussian_noise) to the transmitted signal under a power constraint; discretizing into   
2W  
2*W* dimensions per second ([Nyquist rate](https://grokipedia.com/page/Nyquist_rate)) for bandwidth   
W  
*W*, the capacity simplifies to   
12log⁡2(1+SNR)  
2  
1  
​  
log  
2  
​  
(1+SNR) bits per dimension in the high-resolution limit, where SNR is the [signal-to-noise ratio](https://grokipedia.com/page/Signal-to-noise_ratio)   
P/N  
*P*/*N* with transmit power   
P  
*P* and noise power spectral density   
N/2  
*N*/2.\[1\]  
This capacity   
C  
*C* interprets as the supreme reliable transmission rate in bits per channel use, beyond which [noise](https://grokipedia.com/page/Noise) fundamentally limits error-free communication, even with optimal encoding and decoding.\[1\]

### **Specific Channel Models**

The [binary erasure channel](https://grokipedia.com/page/Binary_erasure_channel) (BEC) models a communication [system](https://grokipedia.com/page/System) where each transmitted bit is received correctly with probability   
1−α  
1−*α* or results in an erasure symbol with probability   
α  
*α*, allowing the receiver to detect but not recover erased bits. Introduced by [Elias](https://grokipedia.com/page/Elias) in his foundational work on coding for noisy channels, the BEC simplifies analysis by separating errors from erasures. The capacity of the BEC is   
C=1−α  
*C*\=1−*α* bits per channel use, derived as the maximum [mutual information](https://grokipedia.com/page/Mutual_information)   
I(X;Y)  
*I*(*X*;*Y*) over input distributions, where the erasure provides partial information. This capacity is achievable with low-complexity codes like parity-check or low-density parity-check (LDPC) codes that detect erasures reliably, as demonstrated by sequences approaching the capacity limit under maximum a posteriori decoding.\[31\]  
Asymmetric binary channels, such as the Z-channel, extend the BEC by introducing biased [error](https://grokipedia.com/page/Error) patterns where one input (typically 0\) is received error-free, while the other (1) flips to 0 with probability   
α  
*α* and stays 1 otherwise. The Z-channel capacity requires numerical optimization over the input distribution   
p=P(X=1)  
*p*\=*P*(*X*\=1), given by   
C=max⁡p\[h(β)−ph(α)\]  
*C*\=max  
*p*  
​  
\[*h*(*β*)−*ph*(*α*)\], where   
β=p(1−α)  
*β*\=*p*(1−*α*) is the probability of output 1 and   
h(⋅)  
*h*(⋅) denotes binary entropy; this formula arises from maximizing   
I(X;Y)=h(Y)−h(Y∣X)  
*I*(*X*;*Y*)=*h*(*Y*)−*h*(*Y*∣*X*), with   
h(Y∣X)=ph(α)  
*h*(*Y*∣*X*)=*ph*(*α*). Coding strategies for the Z-channel often involve asymmetric error-correcting codes, such as repeat-accumulate ensembles, which approach capacity through iterative decoding optimized for the [bias](https://grokipedia.com/page/Bias). Similar optimization techniques apply to other asymmetric binaries like the binary asymmetric channel, where error probabilities differ for each input, yielding capacities via [convex optimization](https://grokipedia.com/page/Convex_optimization) of the [mutual information](https://grokipedia.com/page/Mutual_information).\[32\]  
For continuous-time channels, the [additive white Gaussian noise](https://grokipedia.com/page/Additive_white_Gaussian_noise) (AWGN) channel under a power constraint   
P  
*P* represents a fundamental model, with capacity   
C=Wlog⁡2(1+PN0W)  
*C*\=*W*log  
2  
​  
(1+  
*N*  
0  
​  
*W*  
*P*  
​  
) bits per second for bandwidth   
W  
*W* Hz, where   
N0  
*N*  
0  
​  
 is the noise power spectral density; this seminal result, established by Shannon, assumes Gaussian input distribution to maximize [differential entropy](https://grokipedia.com/page/Differential_entropy). In frequency-selective fading, parallel Gaussian channels with varying noise levels   
σi2  
*σ*  
*i*  
2  
​  
 and total power constraint   
∑Pi≤P  
∑*P*  
*i*  
​  
≤*P* achieve capacity via the [water-filling algorithm](https://grokipedia.com/page/Algorithm), allocating power   
Pi=max⁡(μ−σi2,0)  
*P*  
*i*  
​  
\=max(*μ*−*σ*  
*i*  
2  
​  
,0) such that   
∑Pi=P  
∑*P*  
*i*  
​  
\=*P*, where   
μ  
*μ* is chosen to satisfy the constraint, leading to   
C=∑12log⁡2(1+Piσi2)  
*C*\=∑  
2  
1  
​  
log  
2  
​  
(1+  
*σ*  
*i*  
2  
​  
*P*  
*i*  
​  
​  
). This allocation prioritizes lower-noise subchannels, enhancing [spectral efficiency](https://grokipedia.com/page/Spectral_efficiency) in multicarrier systems like OFDM.\[1\]  
Multiple-input multiple-output (MIMO) channels generalize the Gaussian model to systems with   
nt  
*n*  
*t*  
​  
 transmit and   
nr  
*n*  
*r*  
​  
 receive antennas, where the received signal is   
Y=HX+Z  
**Y**\=**HX**\+**Z**, with channel matrix   
H  
**H**, input [covariance](https://grokipedia.com/page/Covariance)   
Σ  
**Σ** under trace constraint   
tr⁡(Σ)≤P  
tr(**Σ**)≤*P*, and [noise](https://grokipedia.com/page/Noise)   
Z∼N(0,N0I)  
**Z**∼N(0,*N*  
0  
​  
**I**). The ergodic capacity is   
C=max⁡ΣE\[log⁡2det⁡(I+HΣHHN0)\]  
*C*\=max  
**Σ**  
​  
E\[log  
2  
​  
det(**I**\+  
*N*  
0  
​  
**HΣH**  
*H*  
​  
)\] bits per channel use, achieved with Gaussian inputs; for fixed   
H  
**H**, it simplifies to   
log⁡2det⁡(I+HΣHHN0)  
log  
2  
​  
det(**I**\+  
*N*  
0  
​  
**HΣH**  
*H*  
​  
). This formula, derived by Telatar and independently by Foschini, highlights multiplexing gains scaling with   
min⁡(nt,nr)  
min(*n*  
*t*  
​  
,*n*  
*r*  
​  
), enabling high-throughput in wireless systems.\[33\]  
Erasure and deletion channels pose greater challenges than the BEC, as deletions remove symbols without explicit indication, complicating synchronization and decoding. For the binary deletion channel with deletion probability   
δ  
*δ*, the capacity remains an open problem but is bounded above by   
1−h(δ)  
1−*h*(*δ*) and below by constructive codes achieving rates approaching   
1−δ  
1−*δ* for small   
δ  
*δ*; exact capacity expressions are unknown except in limits. The Varshamov-Tenengolts (VT) codes, introduced for single asymmetric errors but adaptable to single deletions, provide near-optimal constructions with rate   
≈1−log⁡nn  
≈1−  
*n*  
log*n*  
​  
 for block length   
n  
*n*, using a parity-check sum   
∑ixi≡0(modn+1)  
∑*ix*  
*i*  
​  
≡0(mod*n*\+1) to locate the deletion. For multiple deletions, bounds rely on combinatorial arguments, with capacity for small   
δ  
*δ* approaching   
1−H2(δ)≈1−δlog⁡2(1/δ)  
1−*H*  
2  
​  
(*δ*)≈1−*δ*log  
2  
​  
(1/*δ*).\[34\]\[35\]  
These channel models inform practical system design, such as in modems where BEC-like erasure handling via [forward error correction](https://grokipedia.com/page/Error_correction_code) improves reliability over [fading](https://grokipedia.com/page/Fading) links, and water-filling optimizes power allocation in DSL modems to combat frequency-dependent [noise](https://grokipedia.com/page/Noise). In 5G New Radio (NR) standards, channel models from [3GPP](https://grokipedia.com/page/3GPP) TR 38.901 incorporate clustered delay line (CDL) and tapped delay line (TDL) profiles for frequencies up to 100 GHz, enabling [MIMO](https://grokipedia.com/page/MIMO) capacity computations under spatial consistency and [beamforming](https://grokipedia.com/page/Beamforming), with implications for enhanced [mobile broadband](https://grokipedia.com/page/Mobile_broadband) achieving up to 20 Gbps peak rates.\[36\]\[37\]

## **Advanced Concepts**

### **Directed Information**

Directed information generalizes [mutual information](https://grokipedia.com/page/Mutual_information) to [stochastic](https://grokipedia.com/page/Stochastic) processes exhibiting temporal dependencies, providing a measure of causal [information transfer](https://grokipedia.com/page/Information_transfer) from one process to another in a directed manner. Formalized by James L. Massey in 1990, building on ideas from Hans Marko's bidirectional [communication theory](https://grokipedia.com/page/Communication_theory), it addresses scenarios where the influence flows asymmetrically over time, such as in communication channels with memory or feedback, where traditional [mutual information](https://grokipedia.com/page/Mutual_information) fails to capture [causality](https://grokipedia.com/page/Causality).\[38\] This measure is particularly valuable in analyzing systems where past outputs influence future inputs, enabling the quantification of [information flow](https://grokipedia.com/page/Information_flow) in non-stationary or sequential settings.\[38\]  
The directed information from an input process   
Xn=(X1,…,Xn)  
*X*  
*n*  
\=(*X*  
1  
​  
,…,*X*  
*n*  
​  
) to an output process   
Yn=(Y1,…,Yn)  
*Y*  
*n*  
\=(*Y*  
1  
​  
,…,*Y*  
*n*  
​  
) is formally defined as

I(Xn→Yn)=∑t=1nI(Xt;Yt∣Yt−1),

*I*(*X*

*n*

→*Y*

*n*

)=

*t*\=1

∑

*n*

​

*I*(*X*

*t*

​

;*Y*

*t*

​

∣*Y*

*t*−1

),

where   
I(⋅;⋅∣⋅)  
*I*(⋅;⋅∣⋅) denotes [conditional mutual information](https://grokipedia.com/page/Conditional_mutual_information),   
Yt−1=(Y1,…,Yt−1)  
*Y*  
*t*−1  
\=(*Y*  
1  
​  
,…,*Y*  
*t*−1  
​  
) (with   
Y0  
*Y*  
0  
 empty), and the sum aggregates the incremental information contributed by each input symbol given the prior output history.\[38\] This formulation emphasizes [causality](https://grokipedia.com/page/Causality) by conditioning only on past outputs, avoiding non-causal dependencies on future values. The directed information rate is then   
Iˉ(X→Y)=lim⁡n→∞1nI(Xn→Yn)  
*I*  
ˉ  
(*X*→*Y*)=lim  
*n*→∞  
​  
*n*  
1  
​  
*I*(*X*  
*n*  
→*Y*  
*n*  
), assuming the limit exists.\[39\]  
For channels with memory, where the output at each time depends on the entire input [history](https://grokipedia.com/page/History) and possibly past outputs, the capacity is characterized using the directed information rate. Specifically, the capacity   
C  
*C* is given by

C=sup⁡lim⁡n→∞1nI(Xn→Yn),

*C*\=sup

*n*→∞

lim

​

*n*

1

​

*I*(*X*

*n*

→*Y*

*n*

),

where the supremum is taken over all causal input distributions   
PXn∥Yn−1  
*P*  
*X*  
*n*  
∥*Y*  
*n*−1  
​  
 that respect the channel's [memory](https://grokipedia.com/page/Memory) structure.\[39\] This multi-letter expression accounts for the temporal correlations, making it suitable for channels like those with inter-symbol interference or additive noise with [memory](https://grokipedia.com/page/Memory).\[39\]  
Key properties of directed information include its non-negativity and the [data processing inequality](https://grokipedia.com/page/Data_processing_inequality),   
I(Xn→Yn)≤I(Xn→Zn)  
*I*(*X*  
*n*  
→*Y*  
*n*  
)≤*I*(*X*  
*n*  
→*Z*  
*n*  
) for a channel from   
Yn  
*Y*  
*n*  
 to   
Zn  
*Z*  
*n*  
.\[38\] It reduces to the standard [mutual information](https://grokipedia.com/page/Mutual_information)   
I(Xn;Yn)  
*I*(*X*  
*n*  
;*Y*  
*n*  
) for memoryless channels or when there is no feedback, as   
I(Xn→Yn)=I(Xn;Yn)  
*I*(*X*  
*n*  
→*Y*  
*n*  
)=*I*(*X*  
*n*  
;*Y*  
*n*  
) holds under [independence](https://grokipedia.com/page/Independence) of the   
Yt  
*Y*  
*t*  
​  
.\[38\] Unlike mutual information, directed information is asymmetric,   
I(Xn→Yn)≠I(Yn→Xn)  
*I*(*X*  
*n*  
→*Y*  
*n*  
)  
\=*I*(*Y*  
*n*  
→*X*  
*n*  
) in general, which explicitly encodes the direction of information flow and distinguishes causal influences.\[38\] The [conditional mutual information](https://grokipedia.com/page/Conditional_mutual_information) referenced here builds on the concept from [mutual information](https://grokipedia.com/page/Mutual_information) analysis, measuring the reduction in uncertainty about   
Yt  
*Y*  
*t*  
​  
 given   
Yt−1  
*Y*  
*t*−1  
.  
In applications to feedback channels, where the input   
Xt  
*X*  
*t*  
​  
 may depend on previous outputs   
Yt−1  
*Y*  
*t*−1  
, directed information provides the appropriate metric for capacity, as mutual [information](https://grokipedia.com/page/Information) assumes non-causal access. The feedback capacity satisfies   
Cfeedback≥Cno feedback  
*C*  
feedback  
​  
≥*C*  
no feedback  
​  
, with equality for discrete memoryless channels but strict increase possible for channels with memory.\[38\] A notable example is the Schalkwijk-Kailath scheme for the [additive white Gaussian noise](https://grokipedia.com/page/Additive_white_Gaussian_noise) channel with feedback, which achieves the feedback capacity through iterative linear encoding that refines message estimates, demonstrating practical gains in error exponents despite no increase in asymptotic capacity for this memoryless case.\[40\] This scheme highlights how directed information guides optimal coding strategies in feedback scenarios by focusing on causal contributions.\[40\]  
Examples of directed information computation arise in Markovian settings, where sources or channels follow a [Markov property](https://grokipedia.com/page/Markov_property), simplifying the conditional terms in the sum. For a [first-order](https://grokipedia.com/page/First-order) Markov source driving a Markov channel, the directed information rate can be evaluated using the [stationary distribution](https://grokipedia.com/page/Stationary_distribution) and transition probabilities, yielding closed-form expressions for the causal flow.\[41\]

### **Information in Non-Standard Settings**

Information theory extends beyond classical discrete and continuous domains to encompass [quantum systems](https://grokipedia.com/page/Quantum-Systems), computational paradigms, and complex stochastic processes, where traditional Shannon entropy must be generalized to capture phenomena like superposition, undecidability, and long-range correlations. In quantum settings, information is quantified using density operators rather than probability distributions, leading to measures that account for non-commutativity and entanglement. Algorithmic variants shift focus from probabilistic uncertainty to the intrinsic [compressibility](https://grokipedia.com/page/Compressibility) of individual objects via program length. These extensions provide foundational tools for fields like [quantum computing](https://grokipedia.com/page/Quantum_computing) and [theoretical physics](https://grokipedia.com/page/Theoretical_physics), revealing limits unattainable in classical frameworks.  
In quantum information theory, the von Neumann entropy serves as the primary measure of uncertainty for a quantum state described by a density matrix   
ρ  
*ρ*, defined as

S(ρ)=−Tr⁡(ρlog⁡ρ),

*S*(*ρ*)=−Tr(*ρ*log*ρ*),

where   
Tr⁡  
Tr denotes the trace operation and the logarithm is base-2 for bits. This entropy generalizes Shannon's entropy to quantum mechanics, quantifying the mixedness of   
ρ  
*ρ* while vanishing for pure states. For an ensemble of states   
{pi,ρi}  
{*p*  
*i*  
​  
,*ρ*  
*i*  
​  
}, the Holevo bound   
χ  
*χ* upper-bounds the accessible classical information, given by

χ=S(∑ipiρi)−∑ipiS(ρi),

*χ*\=*S*(

*i*

∑

​

*p*

*i*

​

*ρ*

*i*

​

)−

*i*

∑

​

*p*

*i*

​

*S*(*ρ*

*i*

​

),

establishing a fundamental limit on how much classical data can be reliably transmitted through quantum channels without measurement collapse. The quantum mutual information between subsystems   
A  
*A* and   
B  
*B* of a bipartite state   
ρAB  
*ρ*  
*AB*  
​  
 extends this to correlations, defined as   
I(A:B)=S(ρA)+S(ρB)−S(ρAB)  
*I*(*A*:*B*)=*S*(*ρ*  
*A*  
​  
)+*S*(*ρ*  
*B*  
​  
)−*S*(*ρ*  
*AB*  
​  
), where   
ρA=Tr⁡B(ρAB)  
*ρ*  
*A*  
​  
\=Tr  
*B*  
​  
(*ρ*  
*AB*  
​  
) and similarly for   
ρB  
*ρ*  
*B*  
​  
; this measure is non-negative and equals twice the entanglement entropy for pure states. Quantum channels, modeled as completely positive trace-preserving maps, have capacities constrained by these quantities; for the qubit depolarizing channel   
Np(ρ)=(1−p)ρ+pI2  
N  
*p*  
​  
(*ρ*)=(1−*p*)*ρ*\+*p*  
2  
*I*  
​  
, where   
p  
*p* is the depolarizing probability and   
I  
*I* is the identity, the classical capacity equals the Holevo information   
χ(Np)  
*χ*(N  
*p*  
​  
), achieved additively even when tensored with arbitrary channels, while the quantum capacity remains open but bounded above by approximate degradability for low   
p  
*p*.\[42\]\[43\]  
Algorithmic information theory redefines information content through the lens of computation, independent of probability. The [Kolmogorov complexity](https://grokipedia.com/page/Kolmogorov_complexity)   
K(x)  
*K*(*x*) of a binary string   
x  
*x* is the length of the shortest program in a fixed [universal Turing machine](https://grokipedia.com/page/Universal_Turing_machine) that outputs   
x  
*x* and halts, providing an absolute, observer-independent measure of complexity. This notion, introduced by [Andrey Kolmogorov](https://grokipedia.com/page/Andrey_Kolmogorov), captures the minimal description length required to specify   
x  
*x*, rendering random strings those with   
K(x)≈∣x∣  
*K*(*x*)≈∣*x*∣ (incompressible), but   
K(x)  
*K*(*x*) is uncomputable due to the [halting problem](https://grokipedia.com/page/Halting_problem), limiting its practical use to approximations like compression algorithms. [Mutual information](https://grokipedia.com/page/Mutual_information) analogs, such as   
I(x:y)=K(x)+K(y)−K(x,y)  
*I*(*x*:*y*)=*K*(*x*)+*K*(*y*)−*K*(*x*,*y*), quantify shared complexity between objects, foundational for understanding [randomness](https://grokipedia.com/page/Randomness) and induction despite theoretical intractability.  
For stochastic processes, the entropy rate quantifies average uncertainty per symbol in the long run. For a stationary discrete-time process   
{Xi}  
{*X*  
*i*  
​  
}, the entropy rate is defined as

H=lim⁡n→∞1nH(X1,…,Xn),

*H*\=

*n*→∞

lim

​

*n*

1

​

*H*(*X*

1

​

,…,*X*

*n*

​

),

where the limit exists under stationarity and equals   
lim⁡n→∞H(Xn∣X1,…,Xn−1)  
lim  
*n*→∞  
​  
*H*(*X*  
*n*  
​  
∣*X*  
1  
​  
,…,*X*  
*n*−1  
​  
) by the chain rule. This rate, originally explored by [Claude Shannon](https://grokipedia.com/page/Claude_Shannon), governs the fundamental limit for [lossless compression](https://grokipedia.com/page/Lossless_compression) of process outputs, with finite values for ergodic processes like Markov chains but infinity for non-stationary ones. It bridges classical information theory to dynamical systems, enabling analysis of correlation decay in sources like language models or physical [time series](https://grokipedia.com/page/Time_series).  
These concepts find applications in quantum gravity, such as the AdS/CFT correspondence, where holographic information posits that bulk gravitational degrees of freedom in anti-de Sitter (AdS) space encode boundary [conformal field theory](https://grokipedia.com/page/Conformal_field_theory) ([CFT](https://grokipedia.com/page/Conformal_field_theory)) information, with entanglement entropy across minimal surfaces bounding the Ryu-Takayanagi formula   
S=Area⁡(γ)4GN  
*S*\=  
4*G*  
*N*  
​  
Area(*γ*)  
​  
, where   
γ  
*γ* is the extremal surface homologous to the boundary region; this duality suggests emergent spacetime from [quantum information](https://grokipedia.com/page/Quantum_information) limits, as explored in generalizations to excited states and deformed geometries.

## **Applications**

### **Communication and Secrecy**

Information theory provides foundational principles for [secure communication](https://grokipedia.com/page/Secure_communication), ensuring that messages remain confidential even against adversaries with unlimited computational power. A cornerstone is the concept of perfect secrecy, introduced by [Claude Shannon](https://grokipedia.com/page/Claude_Shannon), which requires that the [mutual information](https://grokipedia.com/page/Mutual_information) between the [plaintext](https://grokipedia.com/page/Plaintext) and the [ciphertext](https://grokipedia.com/page/Ciphertext) is zero, meaning the adversary gains no information about the message from the ciphertext alone.\[44\] This condition holds if the key used for encryption is at least as long as the message and uniformly random, independent of the message, as demonstrated in the [one-time pad](https://grokipedia.com/page/One-time_pad) scheme where the ciphertext is the modular sum of the message and key.\[44\] In terms of [entropy](https://grokipedia.com/page/Entropy), perfect secrecy demands that the key entropy   
H(K)  
*H*(*K*) satisfies   
H(K)≥H(M)  
*H*(*K*)≥*H*(*M*), where   
H(M)  
*H*(*M*) is the entropy of the message   
M  
*M*, ensuring the key cannot be shorter than the message's uncertainty without compromising security.\[44\]  
In noisy communication environments, the wiretap channel model extends these ideas to scenarios where an eavesdropper receives a degraded version of the signal. Aaron Wyner defined the secrecy capacity as the maximum rate at which a message can be reliably transmitted to the legitimate receiver while keeping it perfectly secret from the eavesdropper, given by   
Cs=max⁡p(x)\[I(X;Y)−I(X;Z)\]  
*C*  
*s*  
​  
\=max  
*p*(*x*)  
​  
\[*I*(*X*;*Y*)−*I*(*X*;*Z*)\], where   
X  
*X* is the input,   
Y  
*Y* the legitimate output, and   
Z  
*Z* the eavesdropper's output.\[45\] For degraded channels, where the eavesdropper's channel is a degraded version of the main channel, this simplifies to   
Cs=Cmain−Cwiretap  
*C*  
*s*  
​  
\=*C*  
main  
​  
−*C*  
wiretap  
​  
, with   
Cmain  
*C*  
main  
​  
 and   
Cwiretap  
*C*  
wiretap  
​  
 being the capacities of the respective channels.\[45\] Achieving this capacity involves stochastic encoding, where the transmitter adds random noise to confuse the eavesdropper without affecting the legitimate receiver's decoding, leveraging the difference in mutual informations.\[45\]  
Authentication and key distribution in information-theoretic settings rely on mutual information measures to bound security, particularly in protocols that generate shared secrets over public channels. [Ueli Maurer](https://grokipedia.com/page/Ueli_Maurer) showed that parties observing correlated random variables can distill a secret key through public discussion, with the achievable key rate bounded by the [mutual information](https://grokipedia.com/page/Mutual_information) between their observations minus leakage to the adversary.\[46\] In [public-key cryptography](https://grokipedia.com/page/Public-key_cryptography) analogs, information-theoretic bounds use the asymptotic equipartition property (AEP) to analyze extractors, such as universal hash functions, which compress high-[entropy](https://grokipedia.com/page/Entropy) sources into uniform keys while preserving secrecy; the AEP ensures that typical sequences have [entropy](https://grokipedia.com/page/Entropy) close to the source's, enabling efficient extraction.\[46\] These extractors guarantee that the output key's [min-entropy](https://grokipedia.com/page/Min-entropy) is nearly the input's, providing strong security guarantees independent of computational assumptions.\[47\]  
Steganography applies information theory to hide messages within cover media such that the presence of the hidden information is undetectable. Christian Cachin formalized this using the Kullback-Leibler (KL) divergence, defining perfect [secrecy](https://grokipedia.com/page/Secrecy) when the [divergence](https://grokipedia.com/page/Divergence) between the distributions of cover and stego (hidden) objects approaches zero, ensuring the adversary cannot distinguish them better than random guessing.\[48\] The embedding rate is limited by the KL divergence, as higher rates increase detectability; secure schemes minimize   
D(Pcover∥Pstego)  
*D*(*P*  
cover  
​  
∥*P*  
stego  
​  
) through careful [distortion](https://grokipedia.com/page/Distortion) of the cover while preserving statistical [properties](https://grokipedia.com/page/.properties).\[48\]  
Practical examples illustrate these principles. In quantum key distribution, the [BB84](https://grokipedia.com/page/BB84) protocol by Charles Bennett and [Gilles Brassard](https://grokipedia.com/page/Gilles_Brassard) enables information-theoretically secure key exchange using polarized photons, where error correction and privacy amplification—via hash-based extractors—distill a secret key from the shared quantum measurements, secure against any eavesdropper due to the [no-cloning theorem](https://grokipedia.com/page/No-cloning_theorem) and entropy extraction.\[49\]

### **Computing and Machine Learning**

Information theory plays a pivotal role in the design and analysis of pseudorandom number generators (PRNGs), where information-theoretic tests evaluate the unpredictability and [entropy](https://grokipedia.com/page/Entropy) of generated sequences to ensure they mimic true [randomness](https://grokipedia.com/page/Randomness) for cryptographic and simulation purposes. These tests, grounded in [entropy](https://grokipedia.com/page/Entropy) measures, assess whether a PRNG's output distribution is indistinguishable from uniform [randomness](https://grokipedia.com/page/Randomness) by quantifying deviations in [conditional entropy](https://grokipedia.com/page/Conditional_entropy) or [mutual information](https://grokipedia.com/page/Mutual_information) between consecutive outputs. For instance, tests based on source coding theory compress PRNG outputs and compare the achieved compression rates against those expected from truly random sources, revealing biases if the [entropy](https://grokipedia.com/page/Entropy) falls short of the theoretical maximum.\[50\]  
A key application in [pseudorandomness](https://grokipedia.com/page/Pseudorandomness) involves [entropy](https://grokipedia.com/page/Entropy) extraction from weak random sources, where the leftover hash lemma provides a foundational result for converting sources with partial [min-entropy](https://grokipedia.com/page/Min-entropy) into nearly uniform keys. The lemma states that, for a source with [min-entropy](https://grokipedia.com/page/Min-entropy)   
k  
*k* and a family of universal hash functions, hashing the source yields an output whose [statistical distance](https://grokipedia.com/page/Statistical_distance) from uniform is at most   
2−ℓ−k2  
2  
−  
2  
ℓ−*k*  
​  
, where   
ℓ  
ℓ is the output length, enabling secure [key generation](https://grokipedia.com/page/Key_generation) even from imperfect [randomness](https://grokipedia.com/page/Randomness) like hardware [noise](https://grokipedia.com/page/Noise). This principle underpins privacy amplification in [cryptography](https://grokipedia.com/page/Cryptography), ensuring that adversaries gain negligible information about the extracted bits.  
In [machine learning](https://grokipedia.com/page/Machine_learning), the information bottleneck (IB) principle formalizes the trade-off between data compression and predictive utility by seeking representations that minimize [mutual information](https://grokipedia.com/page/Mutual_information) with inputs while maximizing it with outputs. Introduced as a method to extract relevant features through a bottleneck, IB optimizes the objective   
I(X;T)−βI(T;Y)  
*I*(*X*;*T*)−*βI*(*T*;*Y*), where   
X  
*X* is the input,   
T  
*T* the compressed representation,   
Y  
*Y* the target, and   
β  
*β* balances compression against relevance. Variational bounds approximate this non-convex optimization, enabling scalable training via neural networks that approximate the posterior   
p(t∣x)  
*p*(*t*∣*x*). This framework has influenced [unsupervised learning](https://grokipedia.com/page/Unsupervised_learning) by promoting parsimonious models that discard irrelevant noise.\[51\]\[52\]  
Neural networks leverage information theory for representation learning, as seen in InfoGAN, which extends generative adversarial networks by maximizing [mutual information](https://grokipedia.com/page/Mutual_information) between latent codes and generated images to yield interpretable, disentangled factors. In InfoGAN, the objective augments the GAN loss with   
I(c;G(z,c))  
*I*(*c*;*G*(*z*,*c*)), where   
c  
*c* is a subset of informative noise, estimated via a variational lower bound to encourage structured latent spaces without supervision. Similarly, rate-distortion theory informs autoencoders by framing encoding as a compression problem, minimizing distortion   
d(x,x^)  
*d*(*x*,  
*x*  
^  
) subject to a rate constraint on the [mutual information](https://grokipedia.com/page/Mutual_information)   
I(x;z)  
*I*(*x*;*z*), where   
z  
*z* is the latent code. This approach yields efficient embeddings for tasks like dimensionality reduction, with the rate-distortion function   
R(D)=min⁡I(X;Z)  
*R*(*D*)=min*I*(*X*;*Z*) such that   
E\[d(X,X^)\]≤D  
*E*\[*d*(*X*,  
*X*  
^  
)\]≤*D*.\[53\]\[54\]  
In [big data](https://grokipedia.com/page/Big_data) analysis, [entropy](https://grokipedia.com/page/Entropy) measures enhance clustering by quantifying the uncertainty reduction achieved by partitioning data into groups. An information-theoretic perspective determines the optimal number of clusters by minimizing the total [entropy](https://grokipedia.com/page/Entropy) across clusters while penalizing complexity, treating clustering as a balance between description length and fit, akin to the minimum description length principle. For example, the [entropy](https://grokipedia.com/page/Entropy) of a clustering is   
H=−∑pklog⁡pk+∑kpkHk  
*H*\=−∑*p*  
*k*  
​  
log*p*  
*k*  
​  
\+∑  
*k*  
​  
*p*  
*k*  
​  
*H*  
*k*  
​  
, where   
pk  
*p*  
*k*  
​  
 is the probability of cluster   
k  
*k* and   
Hk  
*H*  
*k*  
​  
 its internal [entropy](https://grokipedia.com/page/Entropy), guiding algorithms to avoid over- or under-clustering. [Feature selection](https://grokipedia.com/page/Feature_selection) in high-dimensional settings employs [conditional mutual information](https://grokipedia.com/page/Conditional_mutual_information) to identify variables that provide unique predictive power given others, selecting subsets that maximize   
I(f;y∣S)  
*I*(*f*;*y*∣*S*), where   
f  
*f* is a candidate feature,   
y  
*y* the target, and   
S  
*S* the selected set, mitigating redundancy and improving model efficiency.\[55\]\[56\]  
Recent advances as of 2025 integrate information theory with generative models, particularly [diffusion models](https://grokipedia.com/page/Diffusion), where the forward and reverse processes are analyzed through [mutual information](https://grokipedia.com/page/Mutual_information) flows to bound sample quality and training efficiency. In information-theoretic [diffusion](https://grokipedia.com/page/Diffusion) frameworks, the score function aligns with minimum [mean squared error](https://grokipedia.com/page/Mean_squared_error) estimation under [entropy](https://grokipedia.com/page/Entropy) constraints, revealing that diffusion paths preserve and restore information gradients akin to rate-distortion curves in reverse denoising. For large language models (LLMs), [entropy](https://grokipedia.com/page/Entropy) compression bounds limit training efficacy, as the "entropy law" links first-epoch loss to [data](https://grokipedia.com/page/Data) compressibility, showing that LLM [perplexity](https://grokipedia.com/page/Perplexity) scales with the negative log of compression ratios achieved by the model on training corpora. This implies fundamental ceilings on generalization from finite datasets, where [cross-entropy](https://grokipedia.com/page/Cross-entropy) loss cannot drop below the source [entropy](https://grokipedia.com/page/Entropy) without [overfitting](https://grokipedia.com/page/Overfitting).  
