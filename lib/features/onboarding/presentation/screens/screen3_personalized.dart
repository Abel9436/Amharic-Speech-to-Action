import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:goalmate/core/constants/paddings.dart';
import '../../../../core/widgets/app_button.dart';
import '../../../../core/widgets/rive_wrapper.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/text_styles.dart';
import '../bloc/onboarding_bloc.dart';

import '../bloc/onboarding_state.dart';
import '../bloc/onboarding_event.dart';
import 'dart:ui';
import '../../../../core/services/navigation_service.dart';

class Screen3Personalized extends StatelessWidget {
  const Screen3Personalized({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    final screenWidth = MediaQuery.of(context).size.width; // Get screen width
    final riveSize =
        screenWidth * 0.7; // Rive animation will be 70% of screen width

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: Stack(
        children: [
          Positioned(
            top: -100,
            right: -100,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    AppColors.primary.withOpacity(0.1),
                    AppColors.primary.withOpacity(0.05),
                  ],
                ),
              ),
            ),
          ),
          Positioned(
            bottom: -50,
            left: -50,
            child: Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    AppColors.secondary.withOpacity(0.1),
                    AppColors.secondary.withOpacity(0.05),
                  ],
                ),
              ),
            ),
          ),
          Positioned(
            top: MediaQuery.of(context).padding.top + 16,
            left: 24,
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () => context.read<OnboardingBloc>().add(BackPressed()),
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  padding: EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    color: isDarkMode
                        ? AppColors.surfaceDark.withOpacity(0.2)
                        : AppColors.surface.withOpacity(0.05),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isDarkMode
                          ? AppColors.borderColorDark.withOpacity(0.2)
                          : AppColors.border.withOpacity(0.05),
                    ),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.arrow_back_ios_new_rounded,
                        size: 16,
                        color: isDarkMode
                            ? AppColors.textDark
                            : AppColors.text.withOpacity(0.5),
                      ),
                      const SizedBox(width: 4),
                      Text(
                        'Back',
                        style: AppTextStyles.bodySmall.copyWith(
                          color: isDarkMode
                              ? AppColors.textDark
                              : AppColors.text.withOpacity(0.5),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          SafeArea(
            child: SingleChildScrollView(
              child: Padding(
                padding: AppPaddings.screenPadding,
                child: BlocBuilder<OnboardingBloc, OnboardingState>(
                  builder: (context, state) {
                    return Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ClipRRect(
                          borderRadius:
                              BorderRadius.circular(AppPaddings.cardRadius),
                          child: BackdropFilter(
                            filter:
                                ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
                            child: Container(
                              padding: AppPaddings.cardPadding,
                              decoration: BoxDecoration(
                                color: (isDarkMode
                                        ? AppColors.surfaceDark
                                        : Colors.white)
                                    .withOpacity(0.1),
                                borderRadius: BorderRadius.circular(
                                    AppPaddings.cardRadius),
                                border: Border.all(
                                    color: (isDarkMode
                                            ? AppColors.borderColorDark
                                            : Colors.black)
                                        .withOpacity(0.1)),
                              ),
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const SizedBox(height: AppPaddings.mediumGap),
                                  RiveWrapper(
                                      asset: 'assets/rive/mascot.riv',
                                      width: riveSize,
                                      height: riveSize,
                                      stateMachineName: 'State Machine 1',
                                      onTap: () {
                                        context
                                            .read<OnboardingBloc>()
                                            .add(CompleteOnboarding());
                                      }),
                                  const SizedBox(height: AppPaddings.mediumGap),
                                  Text(
                                    'Hi ${state.name}, you\'re all set to ${state.goal}!',
                                    style: AppTextStyles.heading(context)
                                        .copyWith(
                                            color:
                                                Theme.of(context).brightness ==
                                                        Brightness.dark
                                                    ? AppColors.textDark
                                                    : AppColors.textLight),
                                    textAlign: TextAlign.center,
                                  ),
                                  const SizedBox(height: AppPaddings.smallGap),
                                  Wrap(
                                    spacing: AppPaddings.smallGap,
                                    runSpacing: AppPaddings.smallGap,
                                    children: state.selectedInterests
                                        .map((interest) => Chip(
                                              label: Text(interest,
                                                  style: AppTextStyles.chip(
                                                          context)
                                                      .copyWith(
                                                          color: AppColors
                                                              .textDark)),
                                              backgroundColor: AppColors
                                                  .secondary
                                                  .withOpacity(0.8),
                                              shape: RoundedRectangleBorder(
                                                  borderRadius:
                                                      BorderRadius.circular(8)),
                                            ))
                                        .toList(),
                                  ),
                                  const SizedBox(height: AppPaddings.largeGap),
                                  Padding(
                                    padding: const EdgeInsets.symmetric(
                                        horizontal: AppPaddings.mediumGap),
                                    child: AppButton(
                                      label: 'Go to Home',
                                      onPressed: () {
                                        context
                                            .read<OnboardingBloc>()
                                            .add(CompleteOnboarding());
                                      },
                                      gradient: AppColors.greenGradient,
                                      ripple: true,
                                    ),
                                  ),
                                  const SizedBox(height: AppPaddings.mediumGap),
                                ],
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: AppPaddings.largeGap),
                      ],
                    );
                  },
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
