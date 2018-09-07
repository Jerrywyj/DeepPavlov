# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
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

import itertools

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction, brevity_penalty, closest_ref_length, corpus_bleu
from deeppavlov.metrics.google_bleu import compute_bleu
from deeppavlov.core.common.metrics_registry import register_metric

smooth = SmoothingFunction()

@register_metric('bleu_advanced')
def bleu_advanced(y_true, y_predicted, weights=(1,), smoothing_function=smooth.method1, auto_reweigh=False, penalty=True):
    bleu_list = []

    y2 = y_true
    y1 = y_predicted

    bleu_measure = sentence_bleu([y2], y1, weights, smoothing_function, auto_reweigh)
                
    hyp_len = len(y1)
    hyp_lengths = hyp_len
    ref_lengths = closest_ref_length([y2], hyp_len) # 1

    bp = brevity_penalty(ref_lengths, hyp_lengths)
    
    if penalty == True:
        score = bleu_measure
    else:
        score = bleu_measure/bp

    return score

@register_metric('bleu')
def bleu(y_true, y_predicted):
    if isinstance(y_true[0], (tuple, list)):
        y_true = (y[0] for y in y_true)
    return corpus_bleu([[y_t.lower().split()] for y_t in y_true],
                       [y_p.lower().split() for y_p in y_predicted])


@register_metric('google_bleu')
def google_bleu(y_true, y_predicted):
    if isinstance(y_true[0], (tuple, list)):
        y_true = (y[0] for y in y_true)
    return compute_bleu(([y_t.lower().split()] for y_t in y_true),
                        (y_p.lower().split() for y_p in y_predicted))[0]


@register_metric('per_item_bleu')
def per_item_bleu(y_true, y_predicted):
    y_predicted = itertools.chain(*y_predicted)
    if isinstance(y_true[0][0], (tuple, list)):
        y_true = (y[0] for y_list in y_true for y in y_list)
    return corpus_bleu([[y_t.lower().split()] for y_t in y_true],
                       [y_p.lower().split() for y_p in y_predicted])


@register_metric('per_item_dialog_bleu')
def per_item_dialog_bleu(y_true, y_predicted):
    y_true = (y['text'] for dialog in y_true for y in dialog)
    return corpus_bleu([[y_t.lower().split()] for y_t in y_true],
                       [y_p.lower().split() for y_p in y_predicted])