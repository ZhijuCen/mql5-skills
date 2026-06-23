# Nodejs based web server

To organize the server part of our projects, we need a web server. We will use the lightest and most technologically advanced nodejs. Server-side scripts for it can be written in JavaScript, which is the same language used in browsers for interactive web pages. This is convenient from the point of view of unified writing of the client and server parts of the system; the client part of any web service, as a rule, is required sooner or later, for example, for administration, registration, and displaying beautiful statistics on the use of the service.

Anyone who knows MQL5 virtually knows JavaScript, so believe in yourselves. The main differences are discussed in the sidebar.

MQL5 vs JavaScript  

   

JavaScript is an interpreted language, unlike the compiled MQL5. For us as developers, this makes life easier because we don't need a separate compilation phase to get a working program. Don't worry about the efficiency of JavaScript: all JavaScript runtimes use JIT (just-in-time) compilation of JavaScript on demand, i.e., the first time a module is accessed. This process occurs automatically, implicitly, once per session, after which the script is executed in compiled form.   

   

MQL5 refers to languages with static typing, that is, when describing variables, we must explicitly specify their type, and the compiler monitors type compatibility. In contrast, JavaScript is a dynamically typed language: the type of a variable is determined by what value we put in it and can change during the life of the variable. This provides flexibility but requires caution in order to avoid unforeseen errors.  

   

JavaScript is, in a sense, a more object-oriented language than MQL5, because almost all entities in it are objects. For example, a function is also an object, and a class, as a descriptor of the properties of objects, is also an object (of a prototype).  

   

JavaScript itself "collects garbage", i.e., frees the memory allocated by the application program for objects. In MQL5 we have to provide the timely call of delete for dynamic objects.   

   

The JavaScript syntax contains many convenient "abbreviations" for writing constructions that in MQL5 have to be implemented in a longer way. For example, in order to pass a parameter pointing to another function to a certain function in MQL5, we need to describe the type of such a pointer using [typedef](/en/book/basis/functions/functions_typedef), separately define a function that matches this prototype, and only then pass its identifier as a parameter. In JavaScript, you can define the function you're pointing to (in its entirety!) directly in the argument list instead of a pointer parameter.

If you are a web developer or already familiar with nodejs, you can skip the installation and configuration steps.

You can download nodejs from the official site [nodejs.org](https://nodejs.org). Installation is available in different versions, for example, using an installer or unpacking an archive. As a result of the installation, you will receive an executable file in the specified directory node.exe and several supporting files and folders.

If nodejs was not added to the system path by the installer, this can be done for the current Windows user by running the following command in the folder where nodejs is installed (where the file node.exe is located):

```
setx PATH "%CD%"

```

Alternatively, you can edit the Windows environment variables from the system properties dialog (Computer -> Properties -> Extra options -> Environment Variables; the specific dialog type depends on the version of the operating system). In any case, in this way, we will ensure the ability to run nodejs from any folder on the computer, which will be useful to us in the future.

You can check the health of nodejs by running the following commands (in the Windows command line):

```
node -v
npm version

```

The first command outputs the version of nodejs, and the second one outputs the version of an important built-in nodejs service, the npm package manager.

A package is a ready-to-use module that adds specific functionality to nodejs. By itself, nodejs is very small, and without packages, it would require a lot of routine coding.

The most requested packages are stored in a centralized repository on the web and can be downloaded and installed on a specific copy of nodejs or globally (for all copies of nodejs if there are several on the machine). Installing a package to a specific copy is done with the following command:

```
npm install <package name>

```

Run it in the folder where nodejs was installed. This command will place the package locally and will not affect other copies of nodejs that already exist or may appear on the computer later on, with unexpected edits.

We, in particular, need the ws package, which implements the WebSocket protocol. That is, you need to run the command:

```
npm install ws

```

and wait for the process to complete. As a result, the folder <nodejs_install_path>/node_modules/ should contain a new subfolder ws with the necessary content (you can look in the README.md file with the description of the package to make sure it's a WebSocket protocol library).

The package contains implementations of both the server and the client. But instead of the latter, we will write our own in MQL5.

All the functionality of the nodejs server is concentrated in the folder /node_modules. It can be compared in purpose with a standard folder MQL5/Include in MetaTrader 5. When writing application programs in JavaScript, we will include or "import" the necessary modules in a special way, by analogy with including mqh header files using the directive #include in MQL5.
