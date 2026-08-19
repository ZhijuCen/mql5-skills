# Format Conversion

ONNX is an open format, which allows using models from different machine learning toolkits. This format is supported by many frameworks, including [Chainer](https://chainer.org/), [Caffee2](https://caffe2.ai/) and [PyTorch](https://pytorch.org/).

One of the most popular tools for converting models to the ONNX format is Microsoft's [ONNXMLTools](https://learn.microsoft.com/ru-ru/windows/ai/windows-ml/onnxmltools).

ONNXMLTools installation and use instructions are available at the [GitHub repo](https://github.com/onnx/onnxmltools). The following toolkits are currently supported:

- Keras (a wrapper of [keras2onnx converter](https://github.com/onnx/keras-onnx/))
- Tensorflow (a wrapper of [tf2onnx converter](https://github.com/onnx/tensorflow-onnx/))
- scikit-learn (a wrapper of [skl2onnx converter](https://github.com/onnx/sklearn-onnx/))
- Apple Core ML
- Spark ML (experimental)
- LightGBM
- libscm;
- XGBoost;
- H2O
- CatBoost

ONNXMLTools can be easily installed. For installation details and model conversion examples, please see the project page at [https://github.com/onnx/onnxmltools#install](https://github.com/onnx/onnxmltools#install).
