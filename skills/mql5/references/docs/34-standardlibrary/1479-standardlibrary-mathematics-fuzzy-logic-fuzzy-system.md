# Fuzzy systems

Fuzzy system (or fuzzy model) is a mathematical model whose calculation is based on fuzzy logic. Construction of such models is applicable when the subject of study has a weak formalization and its exact mathematical description is too complex or unknown.

The progress of a model construction can be divided into three main stages:

1. Definition of input and output characteristics of a model.
2. Building a knowledge base.
3. Selecting one of the methods of fuzzy inference (Mamdani and Sugeno).

The first stage directly effects the consequent two and determines the future operation of the model.

A knowledge base (rule base) is a set of fuzzy rules of "if, then" type that define the relationship between inputs and outputs of the examined object.

Rule condition describes the current state of the object, and rule conclusion — how this condition affects the object.

There can be two types of terms and conclusions for each rule:

1. simple (link to Csinglcond) — includes one fuzzy variable;
2. complex (link to Cconditions) — includes several fuzzy variables.

Each rule in the system has its weight — importance of a rule in the model. Weighting factors are assigned to a rule within range [0, 1].

Depending on the created knowledge base, the system of fuzzy inference is determined for a model. Fuzzy logical inference is a receipt of conclusion in form of a fuzzy set corresponding to the current value of the inputs with use of knowledge base and fuzzy operations. The two main types of fuzzy inference are Mamdani and Sugeno.
