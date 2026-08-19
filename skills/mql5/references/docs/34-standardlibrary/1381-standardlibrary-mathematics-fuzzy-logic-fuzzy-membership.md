# Membership functions

A membership function is a function that allows to calculate the membership degree of a random element of the universal set to a fuzzy set. Consequently, the domain of a membership function should be within the range [0, 1].

In most cases, the membership function is continuous and monotonic.

| Classes of membership functions | Description |
| --- | --- |
| CConstantMembershipFunction | Class for implementing a membership function as a straight line in parallel with the coordinate axis |
| CCompositeMembershipFunction | Class for implementing a composition of membership functions |
| CDifferencTwoSigmoidalMembershipFunction | Class for implementing the membership function in the form of a difference between two sigmoid functions with the A1, A2, C1 and C2 parameters |
| CGeneralizedBellShapedMembershipFunction | Class for implementing a generalized bell-shaped membership function with A, B and C parameters |
| CNormalCombinationMembershipFunction | Class for implementing a two-sided Gaussian membership function with the B1, B2, Sigma1 and Sigma2 parameters |
| CNormalMembershipFunction | Class for implementing a symmetrical Gaussian membership function with the B and Sigma parameters |
| CP_ShapedMembershipFunction | Class for implementing a pi-shaped membership function with the A, B, C and D parameters |
| CProductTwoSigmoidalMembershipFunction | Class for implementing the membership function in the form of a product of two sigmoid functions with the A1, A2, C1 and C2 parameters |
| CS_ShapedMembershipFunction | Class for implementing an S-like membership function with the A and B parameters |
| CTrapezoidMembershipFunction | Class for implementing a trapezoidal membership function with the X1, X2, X3 and X4 parameters |
| CTriangularMembershipFunction | Class for implementing a triangle membership function with the X1, X2 and X3 parameters |
| CSigmoidalMembershipFunction | Class for implementing a sigmoid membership function with the A and C parameters |
| CZ_ShapedMembershipFunction | Class for implementing a z-like membership function with the A and B parameters. |
| IMembershipFunction | Basic class for all membership function classes. |
