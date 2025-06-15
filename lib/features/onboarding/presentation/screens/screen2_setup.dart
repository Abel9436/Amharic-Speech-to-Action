import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:goalmate/core/constants/paddings.dart';
import '../../../../core/widgets/rive_wrapper.dart';
import '../../../../core/widgets/app_button.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/text_styles.dart';
import '../bloc/onboarding_bloc.dart';
import '../bloc/onboarding_state.dart';
import '../bloc/onboarding_event.dart';
import '../widgets/name_input.dart';
import '../widgets/goal_input.dart';
import '../widgets/interest_chips.dart';
import 'dart:ui'; // Import for ImageFilter
import '../../../../core/services/navigation_service.dart';

class Screen2Setup extends StatelessWidget {
  const Screen2Setup({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;
    final screenWidth = MediaQuery.of(context).size.width;
    final riveSize =
        screenWidth * 0.6; // Rive animation will be 60% of screen width

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: Stack(
        children: [
          // Background shapes
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

          // Back button
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
                padding: AppPaddings.screenPadding, // Use global padding
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: AppPaddings.largeGap),
                    // Enhanced title with animation
                    AnimatedOpacity(
                      opacity: 1.0,
                      duration: const Duration(milliseconds: 500),
                      child: Text(
                        "Let\'s personalize your journey",
                        style: AppTextStyles.heading(context).copyWith(
                            color: isDarkMode
                                ? AppColors.textDark
                                : AppColors.textLight,
                            height: 1.2),
                      ),
                    ),
                    const SizedBox(height: AppPaddings.smallGap),
                    // Enhanced subtitle with animation
                    AnimatedOpacity(
                      opacity: 1.0,
                      duration: const Duration(milliseconds: 700),
                      child: Text(
                        'Tell us a bit about yourself to get started.',
                        style: AppTextStyles.subtitle(context).copyWith(
                            color: isDarkMode
                                ? AppColors.textFadedDark
                                : AppColors.textFadedLight,
                            height: 1.4),
                      ),
                    ),
                    const SizedBox(height: AppPaddings.largeGap),
                    // Enhanced glassmorphism card
                    ClipRRect(
                      borderRadius:
                          BorderRadius.circular(AppPaddings.cardRadius),
                      child: BackdropFilter(
                        filter: ImageFilter.blur(sigmaX: 15.0, sigmaY: 15.0),
                        child: Container(
                          padding:
                              AppPaddings.cardPadding, // Use global padding
                          decoration: BoxDecoration(
                            color: (isDarkMode
                                    ? AppColors.surfaceDark
                                    : Colors.white)
                                .withOpacity(0.15),
                            borderRadius:
                                BorderRadius.circular(AppPaddings.cardRadius),
                            border: Border.all(
                                color: (isDarkMode
                                        ? AppColors.borderColorDark
                                        : Colors.black)
                                    .withOpacity(0.15),
                                width: 1.5),
                            boxShadow: [
                              BoxShadow(
                                color:
                                    (isDarkMode ? Colors.black : Colors.white)
                                        .withOpacity(0.1),
                                blurRadius: 20,
                                spreadRadius: 5,
                              ),
                            ],
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const NameInput(),
                              const SizedBox(height: AppPaddings.mediumGap),
                              const GoalInput(),
                              const SizedBox(height: AppPaddings.mediumGap),
                              Text(
                                'Pick your top 3 interests',
                                style: AppTextStyles.body(context).copyWith(
                                    fontWeight: FontWeight.w600,
                                    color: isDarkMode
                                        ? AppColors.textDark
                                        : AppColors.textLight),
                              ),
                              const SizedBox(height: AppPaddings.smallGap),
                              BlocBuilder<OnboardingBloc, OnboardingState>(
                                builder: (context, state) {
                                  return Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      const InterestChips(),
                                      if (state.interestsError != null)
                                        Padding(
                                          padding: const EdgeInsets.only(
                                              top: AppPaddings.smallGap),
                                          child: Text(
                                            state.interestsError!,
                                            style: AppTextStyles.error(context),
                                          ),
                                        ),
                                    ],
                                  );
                                },
                              ),
                              const SizedBox(height: AppPaddings.largeGap),
                              BlocBuilder<OnboardingBloc, OnboardingState>(
                                builder: (context, state) {
                                  return AppButton(
                                    label: state.isLoading
                                        ? 'Submitting...'
                                        : "I\'m Ready",
                                    onPressed:
                                        state.isFormValid && !state.isLoading
                                            ? () {
                                                context
                                                    .read<OnboardingBloc>()
                                                    .add(SubmitProfile());
                                              }
                                            : null,
                                    gradient: AppColors.greenGradient,
                                    ripple: true,
                                  );
                                },
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(
                        height: AppPaddings.largeGap), // Gap after the card
                    // Enhanced Rive animation container
                    Center(
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: (isDarkMode ? Colors.black : Colors.white)
                              .withOpacity(0.1),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                              color: (isDarkMode ? Colors.white : Colors.black)
                                  .withOpacity(0.1)),
                        ),
                        child: BlocBuilder<OnboardingBloc, OnboardingState>(
                          builder: (context, state) {
                            return RiveWrapper(
                              asset: 'assets/rive/mascot.riv',
                              width: riveSize,
                              height: riveSize,
                              stateMachineName: 'State Machine 1',
                              onTap: () {
                                if (state.isFormValid && !state.isLoading) {
                                  context
                                      .read<OnboardingBloc>()
                                      .add(SubmitProfile());
                                }
                              },
                            );
                          },
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
