var gulp = require('gulp');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');
var rename = require('gulp-rename');

// Style Path
var sassSource = 'assets/styles/sass/**/*.scss',
    cssDest = 'assets/styles/css/';
    cssSource = 'assets/styles/css/*.css';
    minifiedCssDest = 'assets/styles/css.min/';

gulp.task('styles', function(){
    gulp.src(sassSource)
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(cssDest));
});

gulp.task('minify-css', () => {
  gulp.src(cssSource)
    .pipe(cleanCSS({compatibility: 'ie8'}))
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest(minifiedCssDest));
});


gulp.task('watch',function() {
    gulp.watch(sassSource,['styles']);
    gulp.watch(cssSource,['minify-css']);
});

