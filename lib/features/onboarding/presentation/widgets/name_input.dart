import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/onboarding_bloc.dart';
import '../bloc/onboarding_state.dart';
import '../bloc/onboarding_event.dart';
import '../../../../core/constants/colors.dart'; // Import AppColors
import '../../../../core/constants/text_styles.dart'; // Import AppTextStyles

class NameInput extends StatelessWidget {
  const NameInput({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    return BlocBuilder<OnboardingBloc, OnboardingState>(
      builder: (context, state) {
        return TextField(
          onChanged: (value) =>
              context.read<OnboardingBloc>().add(NameChanged(value)),
          style: AppTextStyles.body(context), // Apply body text style to input
          decoration: InputDecoration(
            labelText: 'Your Name',
            labelStyle: AppTextStyles.body(context).copyWith(
                color: isDarkMode
                    ? AppColors.textFadedDark
                    : AppColors
                        .textFadedLight), // Use faded text style for label
            hintText: 'e.g., Abel',
            hintStyle: AppTextStyles.body(context).copyWith(
                color: isDarkMode
                    ? AppColors.textFadedDark.withOpacity(0.6)
                    : AppColors.textFadedLight
                        .withOpacity(0.6)), // Use faded text style for hint
            errorText: state.nameError,
            errorStyle: AppTextStyles.body(context)
                .copyWith(color: Colors.red[300]), // Error style
            filled: true,
            fillColor: isDarkMode
                ? AppColors.inputDark
                : AppColors.inputLight, // Use input colors
            border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(
                    color: AppColors.borderColor)), // Use border color
            enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: AppColors.borderColor)),
            focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(
                    color: AppColors
                        .primary)), // Highlight with primary color on focus
            errorBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide:
                    BorderSide(color: Colors.red)), // Red border for error
            focusedErrorBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.red)),
            contentPadding:
                const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
          ),
        );
      },
    );
  }
}
