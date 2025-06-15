import 'package:flutter/material.dart';

class AppPaddings {
  static const EdgeInsets screenPadding =
      EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0);
  static const EdgeInsets cardPadding = EdgeInsets.all(20.0);
  static const double smallGap = 8.0;
  static const double mediumGap = 16.0;
  static const double largeGap = 28.0;
  static const double cardRadius = 24.0;

  // Old constants, consider removing if not used elsewhere
  static const double screen = 24.0; // Marked for potential removal
  static const double field = 16.0; // Marked for potential removal
  static const double chip = 8.0; // Marked for potential removal
}

class AppRadius {
  // Consider deprecating or merging into AppPaddings
  static const double card = 24.0; // Marked for potential removal
  static const double chip = 16.0; // Marked for potential removal
  static const double button = 16.0; // Marked for potential removal
}
