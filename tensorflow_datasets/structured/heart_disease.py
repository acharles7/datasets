# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Heart disease dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """\
@misc{Dua:2019 ,
author = "Janosi, Steinbrunn and Pfisterer, Detrano",
year = "1988",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml/datasets/Heart+Disease",
institution = "University of California, Irvine, School of Information and Computer Sciences"
}
"""

_DESCRIPTION = """\
This data set contain 13 attributes and labels of heart disease from \
303 participants from Cleveland since Cleveland data was most commonly\
used in modern research.

Attribute by column index
1. age      : age in years
2. sex      : sex (1 = male; 0 = female)
3. cp       : chest pain type
    (1 = typical angina; 2 = atypical angina; 3 = non-anginal pain; 4 = asymptomatic)
4. trestbps : resting blood pressure (in mm Hg on admission to the hospital)
5. chol     : serum cholestoral in mg/dl
6. fbs      : (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)
7. restecg  : resting electrocardiographic results
8. thalach  : maximum heart rate achieved
9. exang    : exercise induced angina (1 = yes; 0 = no)
10. oldpeak : ST depression induced by exercise relative to rest
11. slope   : the slope of the peak exercise ST segment (1 = upsloping; 2 = flat; 3 = downsloping)
12. ca      : number of major vessels (0-3) colored by flourosopy
13. thal    : 3 = normal; 6 = fixed defect; 7 = reversable defect
14. num (the predicted attribute): diagnosis of heart disease (angiographic disease status)
    (0 = < 50% diameter narrowing, no presence of heart disease;
     1 = > 50% diameter narrowing, with increasing severity)
Dataset Homepage: http://archive.ics.uci.edu/ml/datasets/Heart+Disease
"""

class HeartDisease(tfds.core.GeneratorBasedBuilder):
  """Heart disease dataset with 13 attributes."""

  VERSION = tfds.core.Version("0.0.1", "New split API (https://tensorflow.org/datasets/splits)")

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "features": tfds.features.Tensor(shape=(13,), dtype=tf.float32),
            "label": tfds.features.ClassLabel(names=['0', '1', '2', '3', '4'])
        }),
        supervised_keys=("features", "label"),
        homepage='http://archive.ics.uci.edu/ml/datasets/Heart+Disease',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""

    filepath = dl_manager.download('http://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data')
    all_lines = tf.io.gfile.GFile(filepath).read().split("\n")
    records = [l for l in all_lines if ('?' not in l) and l]
    # There is no predefined train/val/test split for this dataset.
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"records": records}
            ),
        ]

  def _generate_examples(self, records):
    """Yields examples."""
    for i, row in enumerate(records):
      features = row.split(',')
      yield i, {
          "features": [float(feature) for feature in features[:-1]],
          "label": features[-1]
      }
