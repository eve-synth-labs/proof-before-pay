/**
 * Original zero-dependency browser inference implementation of scikit-learn's
 * char TF-IDF (ngram 2..4, smooth IDF, sublinear TF, L2 norm) + logistic regression.
 * This file is intentionally isolated from the UI for independent cross-language tests.
 */
export function predict(message, model) {
  if (!model || !Array.isArray(model.features) || !Array.isArray(model.weights)) {
    throw new Error('The local ML model has not loaded.');
  }
  const dictionary = model._lookup || (model._lookup = new Map(model.features.map((f, i) => [f, i])));
  const chars = Array.from(String(message).toLowerCase());
  const counts = new Map();
  for (let i = 0; i < chars.length; i++) {
    for (let n = model.ngram_min; n <= model.ngram_max && i+n <= chars.length; n++) {
      const idx = dictionary.get(chars.slice(i, i+n).join(''));
      if (idx === undefined) continue;
      counts.set(idx, (counts.get(idx) || 0) + 1);
    }
  }
  let normSquared = 0;
  const vector = [];
  for (const [idx, count] of counts) {
    const tf = model.sublinear_tf ? 1 + Math.log(count) : count;
    const v = tf * model.idf[idx];
    vector.push([idx, v]);
    normSquared += v*v;
  }
  let logit = model.intercept;
  if (normSquared > 0) {
    const norm = Math.sqrt(normSquared);
    for (const [idx, v] of vector) logit += model.weights[idx] * v / norm;
  }
  return { score: 1 / (1 + Math.exp(-Math.max(-40, Math.min(40, logit)))), featureCount: counts.size, logit };
}
