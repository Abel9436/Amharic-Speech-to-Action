import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../../../core/widgets/rive_wrapper.dart';
import '../../../../core/widgets/app_button.dart';
import '../../../../core/widgets/theme_toggle.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/text_styles.dart';
import '../bloc/onboarding_bloc.dart';
import '../bloc/onboarding_state.dart';
import '../bloc/onboarding_event.dart';

class Screen1Welcome extends StatelessWidget {
  const Screen1Welcome({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness ==
        Brightness.dark; // Determine current theme mode
    final screenWidth = MediaQuery.of(context).size.width;
    final riveSize =
        screenWidth * 0.7; // Rive animation will be 70% of screen width

    return Scaffold(
      backgroundColor: Theme.of(context)
          .scaffoldBackgroundColor, // Set dynamic background color
      body: Stack(
        children: [
          // Soft shapes (optional) - adjust opacity based on theme
          Positioned(
            top: -60,
            left: -40,
            child: Container(
              width: 180,
              height: 180,
              decoration: BoxDecoration(
                color: (isDarkMode ? Colors.white : Colors.black)
                    .withOpacity(0.05), // Adjust based on theme
                shape: BoxShape.circle,
              ),
            ),
          ),
          Positioned(
            bottom: -40,
            right: -30,
            child: Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                color: (isDarkMode ? Colors.white : Colors.black)
                    .withOpacity(0.04), // Adjust based on theme
                shape: BoxShape.circle,
              ),
            ),
          ),
          SafeArea(
            child: Column(
              children: [
                Align(
                  alignment: Alignment.topRight,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: ThemeToggle(),
                  ),
                ),
                const Spacer(),
                // Rive character
                RiveWrapper(
                  asset: 'assets/rive/mascot.riv',
                  width: riveSize,
                  height: riveSize,
                  stateMachineName: 'State Machine 1',
                  onTap: () {
                    context.read<OnboardingBloc>().add(StartPressed());
                  },
                ),
                const SizedBox(height: 32),
                // Animated title
                AnimatedOpacity(
                  opacity: 1.0,
                  duration: const Duration(milliseconds: 800),
                  child: Text(
                    'Welcome to Your Journey',
                    style: AppTextStyles.heading(context).copyWith(
                      foreground: Paint()
                        ..shader = AppColors.greenGradient
                            .createShader(Rect.fromLTWH(0, 0, 200, 70)),
                      color:
                          null, // Remove explicit color to let shader take effect
                    ), // Use AppTextStyles and AppColors gradient
                    textAlign: TextAlign.center,
                  ),
                ),
                const SizedBox(height: 12),
                AnimatedOpacity(
                  opacity: 1.0,
                  duration: const Duration(milliseconds: 1200),
                  child: Text(
                    'Let\'s create something incredible',
                    style: AppTextStyles.subtitle(context).copyWith(
                      color: isDarkMode
                          ? AppColors.textFadedDark
                          : AppColors
                              .textFadedLight, // Ensure text color adapts to theme
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
                const Spacer(),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: BlocBuilder<OnboardingBloc, OnboardingState>(
                    builder: (context, state) {
                      return AppButton(
                        label: 'Get Started',
                        onPressed: () {
                          context.read<OnboardingBloc>().add(StartPressed());
                        },
                        gradient: AppColors.greenGradient,
                        ripple: true,
                      );
                    },
                  ),
                ),
                const SizedBox(height: 32),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
