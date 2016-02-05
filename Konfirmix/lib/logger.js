/** Copyright (c) 2012-2013, Christopher Jeffrey (https://github.com/chjj/)
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:*/
/**
 * tty.js: logger.js
 * Copyright (c) 2012-2013, Christopher Jeffrey (MIT License)
 */

var slice = Array.prototype.slice
  , isatty = require('tty').isatty;

/**
 * Logger
 */

function logger(level) {
  var args = slice.call(arguments, 1);

  if (typeof args[0] !== 'string') args.unshift('');

  level = logger.levels[level];

  args[0] = '\x1b['
    + level[0]
    + 'm['
    + logger.prefix
    + ']\x1b[m '
    + args[0];

  if ((level[1] === 'log' && !logger.isatty[1])
      || (level[1] === 'error' && !logger.isatty[2])) {
    args[0] = args[0].replace(/\x1b\[(?:\d+(?:;\d+)*)?m/g, '');
  }

  return console[level[1]].apply(console, args);
}

logger.isatty = [isatty(0), isatty(1), isatty(2)];

logger.levels = {
  'log': [34, 'log'],
  'error': [41, 'error'],
  'warning': [31, 'error']
};

logger.prefix = 'tty.js';

logger.log = function() {
  return logger.apply(null, ['log'].concat(slice.call(arguments)));
};

logger.warning = function() {
  return logger.apply(null, ['warning'].concat(slice.call(arguments)));
};

logger.error = function() {
  return logger.apply(null, ['error'].concat(slice.call(arguments)));
};

/**
 * Expose
 */

module.exports = logger;
