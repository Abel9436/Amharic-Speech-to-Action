import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/onboarding_bloc.dart';
import '../bloc/onboarding_state.dart';
import '../bloc/onboarding_event.dart';
import '../../../../core/constants/colors.dart'; // Import AppColors
import '../../../../core/constants/text_styles.dart'; // Import AppTextStyles

const List<String> interests = [
  'Music',
  'Coding',
  'Fitness',
  'Travel',
  'Love',
  'Art',
];

class InterestChips extends StatelessWidget {
  const InterestChips({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    return BlocBuilder<OnboardingBloc, OnboardingState>(
      builder: (context, state) {
        return Wrap(
          spacing: 10,
          runSpacing: 10,
          children: interests.map((interest) {
            final selected = state.selectedInterests.contains(interest);
            return ChoiceChip(
              label: Text(interest),
              selected: selected,
              onSelected: (val) {
                // Only allow selecting if less than 3 are selected
                if (!selected && state.selectedInterests.length < 3) {
                  context.read<OnboardingBloc>().add(InterestToggled(interest));
                } else if (selected) {
                  context.read<OnboardingBloc>().add(InterestToggled(interest));
                }
              },
              selectedColor:
                  AppColors.primary, // Use primary green for selected
              backgroundColor: isDarkMode
                  ? AppColors.inputDark
                  : AppColors.inputLight, // Use input colors
              labelStyle: AppTextStyles.chip(context).copyWith(
                color: selected
                    ? Colors.white // White text on selected chip
                    : isDarkMode
                        ? AppColors.textDark
                        : AppColors.textLight, // Themed text for unselected
              ),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8)), // Sharper corners
              side: BorderSide(
                  color: selected
                      ? AppColors.primary
                      : AppColors.borderColor), // Border based on selection
            );
          }).toList(),
        );
      },
    );
  }
}
