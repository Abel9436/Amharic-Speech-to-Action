import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../theme/theme_cubit.dart';

class ThemeToggle extends StatelessWidget {
  const ThemeToggle({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<ThemeCubit, bool>(
      builder: (context, isDarkMode) {
        return IconButton(
          icon: Icon(
              isDarkMode ? Icons.nightlight_round : Icons.wb_sunny_rounded,
              color: isDarkMode ? Colors.yellow[600] : Colors.green[700]),
          onPressed: () => context.read<ThemeCubit>().toggleTheme(),
          tooltip: isDarkMode ? 'Switch to light mode' : 'Switch to dark mode',
        );
      },
    );
  }
}
