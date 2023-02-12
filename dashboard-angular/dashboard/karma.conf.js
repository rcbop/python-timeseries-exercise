module.exports = function(config) {
  config.set({
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-coverage'),
      require('karma-junit-reporter'),
      require('karma-jasmine-html-reporter'),
      require('@angular-devkit/build-angular/plugins/karma')
    ],
    files: [
      'src/**/*.spec.ts',
    ],
    preprocessors: {
      'src/**/*.js': ['coverage'],
    },
    reporters: ['progress', 'junit', 'coverage'],
    coverageReporter: {
      dir: 'reports/coverage',
      reporters: [
        { type: 'html', subdir: 'report-html' },
        { type: 'lcov', subdir: 'report-lcov' }
      ],
      fixWebpackSourcePaths: true
    },
    junitReporter: {
      outputDir: 'reports',
      useBrowserName: false,
      outputFile: 'angular-dashboard-test-results.xml'
    },
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: false,
    browsers: ['Chrome'],
    customLaunchers: {
      ChromeHeadlessCI: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox']
      }
    },
    singleRun: true,
    restartOnFileChange: false
  });
};
