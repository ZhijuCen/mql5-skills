# Array characteristics

Before giving an account of the syntactic particulars of declaring arrays in MQL5 and practices of working with them, let's consider some basic concepts of constructing the arrays.

The core characteristic of an array is the number of dimensions. In a one-dimension array, its elements are placed one by one, like a row of soldiers, and just one number (index) is sufficient to refer to them. Bar-by-bar prices of opening a financial instrument to the given history depth can be saved in such an array.

In a two-dimensional array, its elements diverge in two logically perpendicular directions, forming a kind of a square (or rectangular, in a general case), two indices being required for each element, i.e., one in each dimension. Such an array could be used to store price quads (Open, High, Low, and Close) for each history bar. Bar numbers would be counted with the first dimension, while the second one is used for numbers from 0 through 3, denoting one of the price types.

A three-dimensional array is the equivalent of a cube (or, more strictly in terms of geometry, right-angled parallelepiped) with three axes. Continuing the example with the array of bar-by-bar prices, we could add to it the third dimension responsible for iterating financial instruments from the Market Watch.

For each dimension, the array has a certain length (size) setting the range of possible indexes. If history is supposed to be loaded for 1,000 bars and 10 instruments, we would get an array sized 1,000 elements in the first dimension, 4 elements in the second one (OHLC), and 10 in the third one.

The product of sizes in all dimensions provides the total number of the array elements; in our case, it is 40,000. In MQL5, it may not exceed 2147483647 (maximum for int).

It is already difficult to imagine a solid shape for a 4-dimensional array because we live in a 3D world. However, MQL5 permits the creation of arrays having up to four dimensions.

It should be noted that you can always use a one-dimensional array instead of a multidimensional one with a random number of dimensions, including more than 4. This is just a matter of arranging the recomputing of several indexes into a continuous one. For example, if a two-dimensional array has 10 columns (dimension 1, axis X) and 5 rows (dimension 2, axis Y), it can be transformed into a one-dimensional array with the same quantity of elements, i.e., 50. In this case, the element index will be obtained by the following formula:

```
index = Y * N + X

```

Here, N is the number of elements in the first dimension, in our case, 10; it is the size of each row; Y is the row number (0..4); and X is the column number (0..9) in the row.

Sizes across dimensions are another characteristic that separates an array from a variable. Thus, the number of dimensions and size in each dimension must be specified in some manner in the description, along with the array name and data type (see [the following section](/en/book/basis/arrays/arrays_declaration)).

You should distinguish between the size of a variable (array element) in bytes and that of an array as the number of elements in it. Theoretically, the full array size in terms of memory it consumes must be the product of the size of one element (depending on the data type) and the number of elements. However, this formula does not always work in practice. Particularly, since strings may have different lengths, it is quite difficult to evaluate the memory volume consumed by a string array.

According to the memory allocation method, arrays can be dynamic or fixed-size.

A fixed-size array is described in the code with exact sizes in all dimensions. It is impossible to resize it later. However, practical tasks often occur, in which the amount of data to be processed is contingent and therefore, it is desirable to resize the array during the algorithm operation. Dynamic arrays exist for this particular purpose. As we will see further, they are described without specifying the first-dimension size and can then be "stretched" or "compacted" using the special MQL5 API functions.

MQL5 Documentation uses ambiguous terminology that names fixed-size array static. This concept is also used for the 'static' modifier that can be applied to the array. If such an array is declared dynamic, then it is simultaneously non-static in terms of memory allocation and static in terms of the 'static' modifier. To exclude ambiguousness, the static character in this book will only mean the declaration attribute.

Along with dynamic and fixed-size arrays, there are special arrays in MQL5 to store quotes and the buffers of technical indicators. Such arrays are named timeseries arrays since their indexes correspond with timing. In fact, these arrays are one-dimensional and dynamic. However, unlike other dynamic arrays, the terminal itself allocates memory for them. We will consider them in the sections dealing with [timeseries](/en/book/applications/timeseries) and [indicators](/en/book/applications/indicators_make).
