import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:rive/rive.dart';

class RiveWrapper extends StatefulWidget {
  final String asset;
  final String? artboard;
  final String? stateMachineName;
  final double? width;
  final double? height;
  final VoidCallback? onTap;

  const RiveWrapper({
    super.key,
    required this.asset,
    this.artboard,
    this.stateMachineName,
    this.width,
    this.height,
    this.onTap,
  });

  @override
  State<RiveWrapper> createState() => _RiveWrapperState();
}

class _RiveWrapperState extends State<RiveWrapper> {
  StateMachineController? _controller;
  SMIInput<bool>? _isHovered;
  SMIInput<bool>? _isPressed;
  Artboard? _artboard;

  @override
  void initState() {
    super.initState();
    _loadRiveFile();
  }

  void _loadRiveFile() {
    rootBundle.load(widget.asset).then(
      (data) async {
        final file = RiveFile.import(data);
        final artboard = file.mainArtboard;
        var controller = StateMachineController.fromArtboard(
          artboard,
          widget.stateMachineName ?? 'State Machine 1',
        );
        if (controller != null) {
          artboard.addController(controller);
          _isHovered = controller.findInput<bool>('isHovered');
          _isPressed = controller.findInput<bool>('isPressed');
        }
        setState(() {
          _artboard = artboard;
          _controller = controller;
        });
      },
    );
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  void _onPointerEnter(PointerEnterEvent event) {
    _isHovered?.value = true;
  }

  void _onPointerExit(PointerExitEvent event) {
    _isHovered?.value = false;
    _isPressed?.value = false;
  }

  void _onPointerDown(PointerDownEvent event) {
    _isPressed?.value = true;
  }

  void _onPointerUp(PointerUpEvent event) {
    _isPressed?.value = false;
    widget.onTap?.call();
  }

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: _onPointerEnter,
      onExit: _onPointerExit,
      child: Listener(
        onPointerDown: _onPointerDown,
        onPointerUp: _onPointerUp,
        child: SizedBox(
          width: widget.width,
          height: widget.height,
          child: _artboard == null
              ? const Center(child: CircularProgressIndicator())
              : Rive(
                  artboard: _artboard!,
                  fit: BoxFit.contain,
                ),
        ),
      ),
    );
  }
}
