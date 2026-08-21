import 'lookup_indices.dart';
import 'types.dart';

class Annotator {
  static NameInfo? annotateSingle(String name, {String? dataPath}) {
    final entry = LookupIndices.lookup(name, dataPath: dataPath);
    if (entry == null) return null;
    return NameInfo.fromEntry(entry);
  }

  static dynamic annotate(String name, {String? dataPath}) {
    if (name.trim().isEmpty) return null;
    final tokens = name.trim().split(RegExp(r'\s+'));
    if (tokens.length == 1) {
      return annotateSingle(tokens.first, dataPath: dataPath);
    }
    return tokens
        .map((t) => annotateSingle(t, dataPath: dataPath))
        .toList();
  }
}
