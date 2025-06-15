import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/material.dart';

class ThemeCubit extends Cubit<bool> {
  ThemeCubit() : super(false); // false for light mode initially

  void toggleTheme() {
    emit(!state); // Toggle the boolean state
  }
}
