# Notes on Machine Learning from reading around the Hussain Paper
The machine learning is essentially curve fitting in many dimensions. It takes in x inputs and a number we want to predict e.g. the band gap. The model then has another parameter $\theta$ which is changed to minimise a loss on the training data. It usually uses a least squares method. The loss function measures how wrong the model's prediction are and this is minimised via training.

$$ L = \frac 1 N \sum_{i=1}^N (y_i - \hat y _i)^2 $$

The paper references five different models,

* **Linear regression** : This is simply using $\hat y = \mathbf w \cdot \mathbf x + b $. It is the most simple but it cannot capture non-linearity. 
* **Ridge regression** is similar to linear regression but the loss function has a penalty $ \lambda || \mathbf w || ^2 $ that stops the weights growing larger. This is called regularisation.
* **k-nearest neighbours (KNN)** is predicing the average $y$ of the $k$ most similar training points. There is no specific training data.
* **Random Forest** is when a decision tree repeatedly splits the data on question like "is Br fraction ? 0.3?". A forest averages hundreds of decision trees, each trained on a random resample of the data. Average reduces the variance.
* **XGBoost** is another tree method but you take the first tree and then use the erros left by the first one to build the second tree. $ \hat y ^{(m)} = \hat y ^{(m-1)}+ \eta h_m ( \mathbf x )$ where $\eta$ is the learning rate. It is usually the stronge model on small tabular data. Therefore it is likely the most appropriate format for.

We need to assign a vector to the categories. For numeric categories thats easy enough because you just assign the magntiude of the quantity as a vector. For categories you use one hot encoding.

Device A = $ \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix} = x_A $

Device B = $ \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix} = x_B$

Device C = $ \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}  = x_C$

(This is basically like defining quantum states in QIT)

Then for a linear model you simply weight each of these devices by some corresponding weight $w$.

A linear model's prediction looks like 
$$ \hat y = w_A x_A + w_B x_B + w_C x_C $$

You can judge a model via several key parameters

* $ \text{RMSE} = \sqrt{\frac 1 N \sum (y_i - \hat y _i)^2}$ is the typical error
* Pearson $r$ measures how linearly predictions track truth. $r^2$ is roughly the fraction of variance explained
* **Overfitting** is a common issue. This is when the fit maps to the points and not to the overall trend. The remedy is to hold back data points the model wasn't trained on as a test and report the errors there. 

The paper keeps discussing dimensionality. The *curse of dimensionality* says that as the number of features grows, the data needed to cover the space growns exponentially. The paper therefore restricts the model to a handful of common materials rather than the whole database.

Not all features will be important in the final values of the data. The SHAP uses Shapley values from game theory which says that a feature's contribution is its average marginal effect on the prediction over all orderings of the features. I.e. if you get rid of the feature from the model how does the model change

Another important feature of **Trees** is that they cannot extrapolate outside of what they have seen.

## Physics Principles Behind the Paper

Lets say you're testing a solar cell and you want to figure out its efficiency. You would illuminate it under differnt light intensities and the cell would have some maximum power point at $(V_{mp},J_{mp})$. The efficiency of a given solar cell is given by the electric power produced from a given light power in. This specific form of efficiency is the power conversion efficiency.

$$ PCE = \frac{J_{mp}V_{mp}}{P_{in}} $$

This numerator is tricky to measure because you don't the point on the graph at which the maximum power is. Instead you define a fill factor,

$$ FF = \frac{J_{mp}V_{mp}}{J_{sc}V_{oc}} $$

This is basically the largest square you can fit into your $J-V$ curve. Now combine these two formulae to get a more usable form of the power conversion efficiency relation,

$$\text{PCE} = \frac{J_{sc}V_{oc}FF}{P_{in}}$$

If you short a circuit the current increases to its maximum value, limited only by the internal resistances of the component or cell that you are measuring.
The current is found by simply adding up the number of electrons collected from the solar cell. This is an integral over the photons per unit area, per unit time, per unit frequency. It is similar to a density of states but since its a current its per unit time as well.

$$ J_{sc} \approx q \int ^{\infty}_{E_g/h} \Phi(\nu) EQE \ d \nu$$

* $\Phi(\nu)$ is the photon flux which is the previously mentioned photons per unit area, per unit time, per unit frequency
* Energy is quantised so a a photon with $h \nu < E_g $ can't excite an electron across a gap, so the integral starts at $\nu = E_g/h $. Everything below the gap is wasted.
* $EQE$ is the external quantum efficiency and measures the fraction of incident photons that produce a collected electron. It is a factor between 0 and 1 and takes into account losses from the quantum potential step.
* $q$ is the standard $I = (eV)/t$

Under no illumination a solar cell is just a standard p-n junction. Therefore it's current characteristic are predicted by the shockley equation. 
$$ J_{\text{dark}}(V)= J_0 \left( e^{qV/k_BT} -1 \right) $$

If you add light in then a current density is produced that is in the opposite direction to the forward bias of the shockley equation,

$$ J(V) = J_0 \left(e^{qV/k_BT}-1 \right)- J_L $$
where $J_L$ is the photogenerated current density. 

At open circuit the net current is zero.

$$ J_{sc} = J_0 \left( e^{qV_{oc}/k_BT} - 1 \right) \implies V_{oc} = \frac{k_BT}{q}\ln \left( \frac{J_{sc}}{J_0}+ 1 \right) $$

## Radiative and Non-Radiative Losses

Radiative recombination is the electron falling into a hole and emitting a photon, which is the reverse of absorption. Kirchoff's law is the one behind this and states that at thermal equillbrium a good absorber of light is also a good emitter at the same wavelength.

Lets say you place a cell into a dark room at room temperature.
1. It absorbs thermal photons at some rate which is the flux of the absorbed photons $\Phi_{abs}$.
2. To remain in equilbrium the cell must emit exactly as much flux back out.

Now if you apply a forward voltage $V$, the carrier product rises, $np = n_i^2 e^{qV/k_BT}$ meaning the emission rises by the same factor. 

This is because the forward bias injects carriers across the junction barrier raising the electron and hole densities. If there is more electrons and holes then the chance of recombination is larger. The voltage then settles such that injection equals recombination.

Non-radiative losses are the losses that we could in theory stop if the architecture of the cell was perfect. Therefore these are the losses that we care about avoiding in the paper.


#Principle of a Solar Cell Lecture (Andrei)

The fill-factor is a rectangle that tells you how square the IV dependence is. The shallower the fill-factor and the less square the fill factor. 

The open circuit voltge is roughly equivalent to the band gap. If you plot the photons emitted for a certain $h \nu$ then you get a blackbody type spectra. 

The short circuit current is the photocurrent. i.e. how much current you can produce from an incident photon and its similar to the quantum efficiency. 