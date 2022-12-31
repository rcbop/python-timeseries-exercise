module.exports = function(config) {
  config.set({
    frameworks: ['jasmine', '@angular-devkit/build-angular', 'coverage'],
    files: [
      'src/**/*.spec.ts',
      'src/**/*.d.ts',
    ],
    preprocessors: {
      'src/**/*.js': ['coverage'],
    },
    reporters: ['progress', 'coverage'],
    coverageReporter: {
      type: 'lcov',
      dir: 'coverage/',
    },
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['Chrome'],
    singleRun: false,
    restartOnFileChange: true,
  });
};
