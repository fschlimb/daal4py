#*******************************************************************************
# Copyright 2014-2018 Intel Corporation
# All Rights Reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License"), the following terms apply:
#
# You may not use this file except in compliance with the License.  You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************

# daal4py Naive Bayes Classification example for shared memory systems

import daal4py as d4p
import numpy as np

# let's try to use pandas' fast csv reader
try:
    import pandas
    read_csv = lambda f, c: pandas.read_csv(f, usecols=c, delimiter=',', header=None).values
except:
    # fall back to numpy loadtxt
    read_csv = lambda f, c: np.loadtxt(f, usecols=c, delimiter=',')


def main():
    # input data file
    infile = "./data/batch/naivebayes_train_dense.csv"
    testfile = "./data/batch/naivebayes_test_dense.csv"

    # Configure a training object (20 classes)
    talgo = d4p.multinomial_naive_bayes_training(20)
    
    # Read data. Let's use 20 features per observation
    data   = read_csv(infile, range(20))
    labels = read_csv(infile, range(20,21))
    labels.shape = (labels.size, 1) # must be a 2d array
    tresult = talgo.compute(data, labels)

    # Now let's do some prediction
    palgo = d4p.multinomial_naive_bayes_prediction(20)
    # read test data (with same #features)
    pdata = read_csv(testfile, range(20))
    plabels = read_csv(testfile, range(20,21))
    plabels.shape = (plabels.size, 1)
    # now predict using the model from the training above
    presult = palgo.compute(pdata, tresult.model)

    # Prediction result provides prediction
    assert(presult.prediction.shape == (pdata.shape[0], 1))

    return (presult, plabels)


if __name__ == "__main__":
    (presult, plabels) = main()
    print("\nNaiveBayes classification results (first 20 observations):\n", presult.prediction[0:20])
    print("\nGround truth (first 20 observations)\n", plabels[0:20])
    print('All looks good!')

