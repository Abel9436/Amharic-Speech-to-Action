import 'package:equatable/equatable.dart';

abstract class OnboardingEvent extends Equatable {
  const OnboardingEvent();
  @override
  List<Object?> get props => [];
}

class StartPressed extends OnboardingEvent {}

class BackPressed extends OnboardingEvent {}

class NameChanged extends OnboardingEvent {
  final String name;
  const NameChanged(this.name);
  @override
  List<Object?> get props => [name];
}

class GoalChanged extends OnboardingEvent {
  final String goal;
  const GoalChanged(this.goal);
  @override
  List<Object?> get props => [goal];
}

class InterestToggled extends OnboardingEvent {
  final String interest;
  const InterestToggled(this.interest);
  @override
  List<Object?> get props => [interest];
}

class SubmitProfile extends OnboardingEvent {}

class CompleteOnboarding extends OnboardingEvent {}
