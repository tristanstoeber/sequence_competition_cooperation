# Competition and Cooperation of Assembly Sequences in Recurrent Neural Networks

**Tristan M. Stöber**<sup>1,2,3,✉️</sup>  
**Andrew B. Lehr**<sup>2,4</sup>  
**Marianne Fyhn**<sup>2,5</sup>  
**Arvind Kumar**<sup>6</sup>

<sup>1</sup>Institute for Neural Computation, Ruhr University Bochum, Germany  
<sup>2</sup>Centre for Integrative Neuroplasticity, University of Oslo, Norway  
<sup>3</sup>Epilepsy Center Frankfurt Rhine-Main, Goethe University Frankfurt, Germany  
<sup>4</sup>Department of Neuro- and Sensory Physiology, University Medical Center Göttingen, Germany  
<sup>5</sup>Department of Biosciences, University of Oslo, Norway  
<sup>6</sup>Department of Computational Science and Technology, KTH Royal Institute of Technology, Sweden  

✉️ Correspondence: [tristan.stoeber@posteo.net](mailto:tristan.stoeber@posteo.net)

## Abstract

Neural activity sequences are ubiquitous in the brain and play pivotal roles in functions such as long-term memory formation and motor control. While conditions for storing and reactivating individual sequences have been thoroughly characterized, it remains unclear how multiple sequences may interact when activated simultaneously in recurrent neural networks. This question is especially relevant for weak sequences, comprised of fewer neurons, competing against strong sequences. Using a non-linear rate model with discrete, pre-configured assemblies, we demonstrate that weak sequences can compensate for their competitive disadvantage either by increasing excitatory connections between subsequent assemblies or by cooperating with other co-active sequences. Further, our model suggests that such cooperation can negatively affect sequence speed unless subsequently active assemblies are paired. Our analysis, validated by an analytically tractable linear approximation, characterizes the conditions for successful sequence progression in isolated, competing, and cooperating sequences, and identifies the distinct contributions of recurrent and feed-forward projections. This proof-of-principle study shows how even disadvantaged sequences can be prioritized for reactivation, a process which has recently been implicated in hippocampal memory processing.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
