# Fuzzy is a library for working with fuzzy logic

Fuzzy logic is a synthesis of the traditional Aristotelian logic when truth is marked as a linguistic variable. Fuzzy logic, equivalent to classical logic, has its own fuzzy logic operations on fuzzy sets defined. There are the same operations for fuzzy sets as well as for ordinary sets, only their calculation is by far more difficult. We should also note that the composition of fuzzy sets constitutes as a fuzzy set.

The main principles of fuzzy logic, setting it apart from classical logic, are the maximum proximity to the reflection of reality and a high level of subjectivity, which can lead to significant errors in calculations.

[Fuzzy model (or system)](/en/docs/standardlibrary/mathematics/fuzzy_logic/fuzzy_system) is a mathematical model whose calculation is based on fuzzy logic. Construction of such models is applicable when the subject of study has a weak formalization and its exact mathematical description is too complex or unknown. The quality of these models' output values (error model) directly depends only on the Expert Advisor, which set up this model. The best option to minimize errors is to draw the most complete and comprehensive model and subsequently adjust it with machine learning on a large training set.

The progress of a model construction can be divided into three main stages:

1. Definition of input and output characteristics of a model.
2. Building a knowledge base.
3. Selecting one of the methods of fuzzy inference ([Mamdani](/en/docs/standardlibrary/mathematics/fuzzy_logic/fuzzy_system/cmamdanifuzzysystem) or [Sugeno](/en/docs/standardlibrary/mathematics/fuzzy_logic/fuzzy_system/csugenofuzzysystem)).

The first stage directly effects the consequent two and determines the future operation of the model. A knowledge base or, as sometimes called, [rule](/en/docs/standardlibrary/mathematics/fuzzy_logic/fuzzy_rule) base is a set of fuzzy rules type: "if, then" that define the relationship between inputs and outputs of the examined object. The number of rules in the system is not limited and is also determined by the Expert Advisor. The generalized format of fuzzy rules is as follows:

If rule condition, then rule conclusion.

Rule condition describes the current state of the object, and rule conclusion — how this condition affects the object. General view of conditions and conclusions cannot be selected because they are determined by a fuzzy inference.

Each rule in the system has its weight — this characteristic defines the importance of a rule in the model. Weighting factors are assigned to a rule within range [0, 1]. In many examples with fuzzy models, which can be found in the relevant literature, weight data is not specified, but it does not mean that it is not present. In fact, in such case for each rule from the database, the weight is fixed and equals unity. There can be two types of terms and conclusions for each rule:

1. simple — includes one [fuzzy variable](/en/docs/standardlibrary/mathematics/fuzzy_logic/fuzzy_variable);
2. complex — includes several fuzzy variables.

Depending on the created knowledge base, the system of fuzzy inference is determined for a model. Fuzzy logical inference is a receipt of conclusion in form of a fuzzy set corresponding to the current value of the inputs with use of knowledge base and fuzzy operations. The two main types of fuzzy inference are Mamdani and Sugeno.
