import 'package:flutter/material.dart';

class AppColors {
  static const Color primary = Color(0xFF4CAF50);
  static const Color primaryDark = Color(0xFF16A34A);
  static const Color secondary = Color(0xFF2196F3);
  static const Color accent = Color(0xFFFFC107);
  static const Color error = Color(0xFFE53935);
  static const Color success = Color(0xFF43A047);
  static const Color warning = Color(0xFFFFA000);
  static const Color info = Color(0xFF039BE5);
  static const Color surface = Color(0xFFF5F5F5);
  static const Color border = Color(0xFFE0E0E0);
  static const Color text = Color(0xFF212121);
  static const Color textLight = Color(0xFF757575);
  static const Color textDark = Color(0xFFE0E0E0);
  static const Color background = Color(0xFFFFFFFF);
  static const Color backgroundDark = Color(0xFF1A1A1A);
  static const Color textFadedLight = Color(0xFF9E9E9E);
  static const Color textFadedDark = Color(0xFFB0B0B0);
  static const Color inputLight = Color(0xFFF5F5F5);
  static const Color inputDark = Color(0xFF2C2C2C);
  static const Color borderColor = Color(0xFFE0E0E0);
  static const Color borderColorDark = Color(0xFF404040);
  static const Color accentGray = Color(0xFF6B7280);
  static const Color errorRed = Color(0xFFEF4444);

  static const Color bgDark = Color(0xFF1A1A1A);
  static const Color bgLight = Color(0xFFF8F8F8);
  static const Color surfaceDark = Color(0xFF2C2C2C);

  static const LinearGradient greenGradient = LinearGradient(
    colors: [Color(0xFF4CAF50), Color(0xFF43A047)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient aquaGradient = LinearGradient(
    colors: [
      Color(0xFF67E8F9),
      Color(0xFF38BDF8)
    ], // A refreshing aqua gradient
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
