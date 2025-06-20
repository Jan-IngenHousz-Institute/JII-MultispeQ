.. role:: python(code)
   :language: python
.. role:: javascript(code)
   :language: javascript


Code Porting
============

The PhotosynQ platform provides numerous measurement protocols for use with MultispeQ devices. Each protocol contains JSON-encoded instructions that define how the MultispeQ performs measurements and can be used directly without modification.

However, analyzing the data stream returned by MultispeQ devices requires custom scripts or macros. Since the PhotosynQ platform uses JavaScript for data analysis, these scripts must be converted to Python for use in Python-based workflows.

Beyond standard JavaScript functions, PhotosynQ provides specialized helper functions for common operations and mathematical computations not available in JavaScript's native Math object. When porting code to Python, these helper functions can typically be replaced with native Python functions or established libraries like NumPy and SciPy.

The following reference lists will assist in converting JavaScript analysis code to Python, particularly when working with PhotosynQ's custom `helper functions <https://github.com/Photosynq/helpers>`_.

Array Functions
---------------

MultispeQ devices record fluorescence and absorbance traces as one-dimensional arrays of numerical values. When measurements involve multiple LEDs, the recorded data from all LEDs is combined into a single array where values cycle through each LED in sequence. For example, if LEDs 1, 2, and 3 are used during measurement, the resulting trace array follows the pattern [1,2,3,1,2,3,…], with each position representing data from the corresponding LED.

The functions listed below simplify the process of extracting individual LED traces from these combined arrays. For additional details on trace data structure and analysis, consult the `PhotosynQ Help documentation <help.photosynq.com>`_.

.. list-table:: JavaScript Helper Functions
   :widths: 30 30 40
   :header-rows: 1

   * - JavaScript
     - Python
     - Description
   * - :javascript:`ArrayNth(array, size, start);`
     - :python:`array[start::step]`
     - Extract every n-th element from an array.
   * - :javascript:`ArrayRange(start, stop, step);`
     - :python:`np.arange(start, stop, step)`
     - Generate an array of arithmetic progressions. `numpy.arange <https://numpy.org/doc/stable/reference/generated/numpy.arange.html>`_
   * - :javascript:`ArrayRange(start, stop, step, "x2");`
     - :python:`[x ** 2 for x in np.arange(start, stop, step)]`
     - Generate a progression and transform numbers. (e.g. `x²`  )
   * - :javascript:`ArrayUnZip(array);`
     - :python:`x, y = zip(*array)` \

       :python:`{'x': list(x), 'y': list(y)}`
     - This function transforms an array of [x, y] pairs into an object with an array of x and an array of y values. `zip <https://docs.python.org/3/library/functions.html#zip>`_
   * - :javascript:`ArrayZip(array_x, array_y);`
     - :python:`[list(x) for x in zip(array_x, array_y)]`
     - This function transforms two lists into one list of x,y pairs

Mathmatical Functions
---------------------

.. list-table:: JavaScript Helper Functions
   :widths: 30 30 40
   :header-rows: 1

   * - JavaScript
     - Python
     - Description
   * - :javascript:`MathLN(x);`
     - :python:`np.log(x)`
     - Returns the natural logarithm (base E) of a number `numpy.log <https://numpy.org/doc/stable/reference/generated/numpy.log.html>`_
   * - :javascript:`MathLOG(x);`
     - :python:`np.log10(x)`
     - Returns the logarithm (base 10) of a number `numpy.log10 <https://numpy.org/doc/stable/reference/generated/numpy.log10.html>`_
   * - :javascript:`MathMAX(x);`
     - :python:`np.max(array)`
     - Get the maximum value from an array of numbers `numpy.max <https://numpy.org/doc/stable/reference/generated/numpy.max.html>`_
   * - :javascript:`MathMEAN(array);`
     - :python:`np.mean(array)`
     - Calculate the mean from an array of numbers `numpy.mean <https://numpy.org/doc/stable/reference/generated/numpy.mean.html>`_
   * - :javascript:`MathMEDIAN(array);`
     - :python:`np.median(array)`
     - Calculate the median from an array of numbers `numpy.median <https://numpy.org/doc/stable/reference/generated/numpy.median.html>`_
   * - :javascript:`MathMIN(array);`
     - :python:`np.min(array)`
     - Get the minimum value from an array of numbers `numpy.min <https://numpy.org/doc/stable/reference/generated/numpy.min.html>`_
   * - :javascript:`MathROUND(x, decimals);`
     - :python:`np.round(x, decimals)`
     - Round a given number (float) to a set number of decimals `numpy.round <https://numpy.org/doc/stable/reference/generated/numpy.round.html>`_
   * - :javascript:`MathSTDERR(array);`
     - :python:`np.std(array) / np.sqrt(len(array))`
     - Calculate the standard error from an array of numbers
   * - :javascript:`MathSTDEV(array);`
     - :python:`np.std(array)`
     - Calculate the standard deviation (population) from an array of numbers `numpy.std <https://numpy.org/doc/stable/reference/generated/numpy.std.html>`_
   * - :javascript:`MathSTDEVS(array);`
     - :python:`np.std(array, ddof=1)`
     - Calculate the standard deviation (sample) from an array of numbers `numpy.std <https://numpy.org/doc/stable/reference/generated/numpy.std.html>`_
   * - :javascript:`MathSUM(array);`
     - :python:`np.sum(array)`
     - Calculate the sum from an array of numbers `numpy.sum <https://numpy.org/doc/stable/reference/generated/numpy.sum.html>`_
   * - :javascript:`MathVARIANCE(array);`
     - :python:`np.var(array, ddof=1)`
     - Calculate the variance from an array of numbers `numpy.var <https://numpy.org/doc/stable/reference/generated/numpy.var.html>`_


Regression Functions
--------------------

.. list-table:: **MathEXPINVREG**, Fit exponential decay to Y = Y0 + Ae^(-x/t). A and t are the fitted variables, the provided input array needs to be an array of x,y pairs.
   :widths: 50 50
   :header-rows: 1

   * - Language
     - Code
   * - JavaScript
     - .. code-block:: javascript
         
          MathEXPINVREG( [ [x1,y1], [x2,y2], ..., [xn,yn] ] );
   * - Python
     - .. code-block:: python

          import numpy as np
          from scipy.optimize import curve_fit

          def exponential_decay(x, A, t, asymptote):
              """Exponential decay function: y = A * exp(x * t) + asymptote"""
              return A * np.exp(x * t) + asymptote

          # Fit the curve
          popt, pcov = curve_fit(exponential_decay, x_data, y_data, 
                                p0=[1.0, -0.1, 0.0])  # Initial parameter guesses

          A, t, asymptote = popt

          # Generate fitted points
          y_fitted = exponential_decay(x_data, A, t, asymptote)

          # Calculate R-squared
          ss_res = np.sum((y_data - y_fitted) ** 2)
          ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
          r_squared = 1 - (ss_res / ss_tot)

          # Results equivalent to your JS function
          results = {
              'parameters': [A, t, asymptote],
              'fitted_points': list(zip(x_data, y_fitted)),
              'r_squared': r_squared,
              'lifetime': -1/t,
              'slope': -A * t
          }

.. list-table:: **MathLINREG**, Function to perform a simple linear regression (y = mx +b), returning slope, y-intercent, correlation coefficient (R) and coefficient of determination (R²).
   :widths: 50 50
   :header-rows: 1

   * - Language
     - Code
   * - JavaScript
     - .. code-block:: javascript
         
          MathLINREG([x1, x2, ..., xn], [y1, y2, ..., yn]);
   * - Python
     - .. code-block:: python
         
         scipy import stats
         slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)



.. list-table:: **MathMULTREG**, Multiple Linear Regression
   :widths: 50 50
   :header-rows: 1

   * - Language
     - Code
   * - JavaScript
     - .. code-block:: javascript
         
          MathMULTREG( [ 
            [ [x1,y1], [x2,y2], ..., [xn,yn] ],
            [ [x1,y1], [x2,y2], ..., [xn,yn] ] 
          ]);
   * - Python
     - .. code-block:: python

          import numpy as np
          from sklearn.linear_model import LinearRegression
          from sklearn.metrics import r2_score

          # Extract features (X) and target (y)
          X = np.array([[point[i] for i in range(len(point)-1)] for point in input_raw])
          y = np.array([point[-1] for point in input_raw])

          # Fit the model
          model = LinearRegression()
          model.fit(X, y)

          # Get predictions
          y_pred = model.predict(X)

          # Results equivalent to your JS function
          results = {
              'rsquared': model.score(X, y),  # or r2_score(y, y_pred)
              'slopes': [model.intercept_] + model.coef_.tolist(),  # [intercept, coef1, coef2, ...]
              'points': [X.T.tolist(), y_pred.tolist()]  # [features, predictions]
          }

.. list-table:: **MathPOLYREG**, Polynomial fit to y = a0 + a1x + a2x^2 + a3x^3....
   :widths: 50 50
   :header-rows: 1

   * - Language
     - Code
   * - JavaScript
     - .. code-block:: javascript
         
          MathPOLYREG( [ 
            [ [x1,y1], [x2,y2], ..., [xn,yn] ], 
            [ [x1,y1], [x2,y2], ..., [xn,yn] ] 
          ], degree );
   * - Python
     - .. code-block:: python
         
          import numpy as np

          # Fit polynomial of specified degree
          coefficients = np.polyfit(x_data, y_data, degree)

          # Generate fitted points
          y_fitted = np.polyval(coefficients, x_data)

          # Calculate error (mean squared error)
          error = np.sum((y_fitted - y_data) ** 2) / (len(y_data) - 1)

          # Results equivalent to your JS function
          results = {
              'slopes': coefficients.tolist(),  # [a_n, a_(n-1), ..., a_1, a_0]
              'points': list(zip(x_data, y_fitted)),
              'error': error
          }

.. list-table:: **NonLinearRegression**
   :widths: 50 50
   :header-rows: 1

   * - Language
     - Code
   * - JavaScript `Source <https://help.photosynq.com/macros/provided-functions.html#nonlinearregression>`_
     - .. code-block:: javascript
         
          NonLinearRegression(
            [
              [x1, y1],
              [x2, y2],
              ...,
              [xn, yn]
            ],
            {
                equation: "b + a * e(- x / c)",
                initial: [a, b, c]
            }
          );
   * - Python `scipy.optimize.curve_fit <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html#scipy.optimize.curve_fit>`_
     - .. code-block:: python
         
         from scipy.optimize import curve_fit

         def exp_func(x, a, b, c):
           return b + a * np.exp(-x / c)

         try:
          # Fit the data
          popt, pcov = curve_fit(exp_func, x, y, p0=[1, 1, 1])
          a, b, c = popt
          ...

         except Exception as e:
           pass  # Or handle the error as needed


Trace Transformation
--------------------

If you have two traces of equal length or a trace and a number, the helper function `TransformTrace` allows to transform a given trace (array) based on the second input (array or number) and the provided function.

.. code-block:: javascript
   
   // Two arrays
   TransformTrace("function", array_1, array_2);

   // One array and one number
   TransformTrace("function", array_1, number);

Using Python this can be achieved using native code or the `numpy` module. The code provided shows examples based on the functions available in JavaScript.

.. list-table:: TransformTrace, The function transforms a given array by providing a second same length array, or a single number.
   :widths: 10 50 40
   :header-rows: 1

   * - Function
     - Python Equivalent
     - Description
   * - `add` or `+`
     - :python:`np.array(array_1) + np.array(array_2)` \

       :python:`np.array(array_1) + number`
     - Add array or number to array
   * - `subtract` or `-`
     - :python:`np.array(array_1) - np.array(array_2)` \

       :python:`np.array(array_1) - number`
     - Subtract array or number from array
   * - `multiply` or `*`
     - :python:`np.array(array_1) * np.array(array_2)` \

       :python:`np.array(array_1) * number`
     - Multiply array with array or number
   * - `divide` or `/`
     - :python:`np.array(array_1) / np.array(array_2)` \

       :python:`np.array(array_1) / number`
     - Divide array by array or number
   * - `normToMin`
     - :python:`[x/np.min(array) for x in array]`
     - Normalize to minimum
   * - `normToMax`
     - :python:`[x/np.min(array) for x in array]`
     - Normalize to maximum
   * - `normToRange`
     - :python:`[(x - np.min(array)) / (np.max(array) - np.min(array)) for x in array]`
     - Normalize to the min/max range of the array
   * - `normToIdx`
     - :python:`[x/array[index] for x in array]`
     - Normalize to number found at a specific position (index) in array
   * - `normToVal`
     - :python:`[x/value for x in array]`
     - Normalize to defined value
   * - `ma`
     - :python:`window_size=3` \
       
       :python:`np.convolve(data, np.ones(window_size)/window_size, mode='valid')`
     - Smoothing using a moving average with a selectable window size
   * - `sgf`
     - :python:`from scipy.signal import savgol_filter` \
     
       :python:`savgol_filter(data, window_length=5, polyorder=2)`
     - Smoothing using a Savitzky-Golay Filter `SciPy.signal <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html#scipy.signal.savgol_filter>`_
   * - `abs`
     - :python:`I0 = array[0]` \
     
       :python:`[-np.log10(x/array[0]) for x in array]`
     - Calculate the absorbance using the first value as I0 or a defined I0

Data Lookup
-----------

Function to look up data from sub protocols are implemented in this library and can be used the same way as their JavaScript equivalent.
They are part of the :mod:`jii_multispeq.analysis.basic` module. 

.. code-block:: python

   ## import the analysis module
   import jii_multispeq.analysis as analysis

   data = analysis.GetIndexByLabel()

   ## import a specific function (similar to JavaScript code)
   import jii_multispeq.analysis.GetIndexByLabel as GetIndexByLabel

   data = GetIndexByLabel()


.. list-table:: Data Lookup Functions
   :header-rows: 1

   * - Function
     - Description
   * - :func:`GetIndexByLabel <jii_multispeq.analysis.basic.GetIndexByLabel>`
     - Generate a protocol lookup table for a protocol set
   * - :func:`GetLabelLookup <jii_multispeq.analysis.basic.GetLabelLookup>`
     - Returns the protocol from within the protocol set matching the provided label
   * - :func:`GetProtocolByLabel <jii_multispeq.analysis.basic.GetProtocolByLabel>`
     - Find the positions for protocols within a protocol set matching the provided label


Native JavaScript Math Functions
--------------------------------

The native JavaScript Math Object provides methods for mathematical constants that can be used with Macros on the PhotosynQ platform and don't require any additional import of libraries or functions.
See `JavaScript Math <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math>`_ for available methods and constants.

.. code-block:: javascript
   
   // Math Object as used in a PhotosynQ Macro
   Math.<name>


Native JavaScript Functions
---------------------------

Native JavaScript functions to manipulate arrays and their Python equivalent.

.. list-table:: Native JavaScript Functions
   :widths: 30 30 40
   :header-rows: 1

   * - JavaScript
     - Python
     - Description
   * - :javascript:`array.splice(start,end);`
     - :python:`array[start:end]`
     - Copy part of an array

Notifications
-------------

The functions :javascript:`info("Message" , output)`, :javascript:`warning("Message" , output)`, and :javascript:`danger("Message" , output)` add messages to the output of the macro by category. Currently they are not supported and can be replaced by :python:`print("Message")` to output issues.
