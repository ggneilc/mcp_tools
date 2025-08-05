window.MathJax = {
  tex: {
    packages: {
        '[+]': ['amsmath']      // load the amsmath extension
      },
    inlineMath: [
      ['$', '$'],        // enable single-dollar
      ['\\(', '\\)']     // keep \(…\) as well
    ],
    // (optional) prevent conflict with $$$ display math:
    displayMath: [['$$','$$']]
  }
};
