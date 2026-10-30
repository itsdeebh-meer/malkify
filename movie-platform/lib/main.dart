import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

const tmdbToken = String.fromEnvironment('TMDB_TOKEN');

void main() => runApp(const MalkifyMoviesApp());

class MalkifyMoviesApp extends StatelessWidget {
  const MalkifyMoviesApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Malkify Movies',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF8B5CF6),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFF0B1020),
        cardTheme: const CardThemeData(
          color: Color(0xFF151D32),
          elevation: 0,
          margin: EdgeInsets.zero,
        ),
      ),
      home: const MoviesHomePage(),
    );
  }
}

class MoviesHomePage extends StatefulWidget {
  const MoviesHomePage({super.key});

  @override
  State<MoviesHomePage> createState() => _MoviesHomePageState();
}

class _MoviesHomePageState extends State<MoviesHomePage> {
  final searchController = TextEditingController();
  final Set<int> savedMovieIds = <int>{};
  List<Map<String, dynamic>> movies = <Map<String, dynamic>>[];
  bool showSavedOnly = false;
  bool isLoading = true;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    loadSavedMovies();
    loadMovies();
  }

  Future<void> loadSavedMovies() async {
    final preferences = await SharedPreferences.getInstance();
    final values = preferences.getStringList('savedMovies') ?? <String>[];
    if (!mounted) return;
    setState(() {
      savedMovieIds.addAll(values.map(int.parse));
    });
  }

  Future<void> toggleSavedMovie(int id) async {
    setState(() {
      if (!savedMovieIds.add(id)) {
        savedMovieIds.remove(id);
      }
    });
    final preferences = await SharedPreferences.getInstance();
    await preferences.setStringList(
      'savedMovies',
      savedMovieIds.map((value) => value.toString()).toList(),
    );
  }

  Future<void> loadMovies([String query = '']) async {
    if (tmdbToken.isEmpty) {
      setState(() {
        errorMessage = 'Add your TMDB token with --dart-define=TMDB_TOKEN=...';
        isLoading = false;
      });
      return;
    }

    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    try {
      final path = query.trim().isEmpty ? '/movie/popular' : '/search/movie';
      final uri = Uri.https('api.themoviedb.org', '3$path', {
        'query': query.trim(),
        'language': 'en-US',
        'page': '1',
      });
      final response = await http.get(
        uri,
        headers: {
          'Authorization': 'Bearer $tmdbToken',
          'accept': 'application/json',
        },
      );
      if (response.statusCode != 200) {
        throw Exception('TMDB returned HTTP ${response.statusCode}');
      }
      final payload = jsonDecode(response.body) as Map<String, dynamic>;
      final results = (payload['results'] as List? ?? <dynamic>[])
          .whereType<Map<String, dynamic>>()
          .toList();
      if (mounted) {
        setState(() {
          movies = results;
          errorMessage = '';
        });
      }
    } catch (error) {
      if (mounted) setState(() => errorMessage = error.toString());
    } finally {
      if (mounted) setState(() => isLoading = false);
    }
  }

  List<Map<String, dynamic>> get visibleMovies {
    if (!showSavedOnly) return movies;
    return movies
        .where((movie) => savedMovieIds.contains(movie['id']))
        .toList();
  }

  void showMovieDetails(Map<String, dynamic> movie) {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      backgroundColor: const Color(0xFF151D32),
      builder: (context) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(24, 8, 24, 28),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  movie['title']?.toString() ?? 'Untitled',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 12),
                Text(movie['overview']?.toString().isNotEmpty == true
                    ? movie['overview'].toString()
                    : 'No synopsis is available.'),
                const SizedBox(height: 14),
                Text('Rating: ${movie['vote_average'] ?? 'N/A'} / 10'),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Malkify Movies'),
        backgroundColor: const Color(0xFF0B1020),
        actions: [
          IconButton(
            tooltip: showSavedOnly ? 'Show popular movies' : 'Show saved movies',
            onPressed: () => setState(() => showSavedOnly = !showSavedOnly),
            icon: Icon(
              showSavedOnly
                  ? Icons.local_movies_outlined
                  : Icons.bookmarks_outlined,
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: searchController,
              textInputAction: TextInputAction.search,
              onSubmitted: loadMovies,
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.search),
                hintText: 'Search movies',
                filled: true,
                fillColor: const Color(0xFF151D32),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(14),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),
          if (errorMessage.isNotEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text(
                errorMessage,
                style: const TextStyle(color: Colors.orangeAccent),
              ),
            ),
          if (isLoading)
            const Expanded(child: Center(child: CircularProgressIndicator()))
          else if (visibleMovies.isEmpty)
            const Expanded(
              child: Center(child: Text('No movies to show yet.')),
            )
          else
            Expanded(
              child: GridView.builder(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 20),
                gridDelegate:
                    const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  childAspectRatio: 0.58,
                  crossAxisSpacing: 14,
                  mainAxisSpacing: 14,
                ),
                itemCount: visibleMovies.length,
                itemBuilder: (context, index) {
                  final movie = visibleMovies[index];
                  final id = movie['id'] as int;
                  final posterPath = movie['poster_path']?.toString();
                  return Card(
                    clipBehavior: Clip.antiAlias,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                      side: const BorderSide(color: Color(0xFF293653)),
                    ),
                    child: InkWell(
                      onTap: () => showMovieDetails(movie),
                      child: Column(
                        children: [
                          Expanded(
                            child: posterPath == null
                                ? const Center(
                                    child: Icon(Icons.movie, size: 42),
                                  )
                                : Image.network(
                                    'https://image.tmdb.org/t/p/w500$posterPath',
                                    width: double.infinity,
                                    fit: BoxFit.cover,
                                    errorBuilder: (context, error, stack) =>
                                        const Center(
                                      child: Icon(Icons.movie, size: 42),
                                    ),
                                  ),
                          ),
                          Padding(
                            padding: const EdgeInsets.fromLTRB(8, 10, 8, 0),
                            child: Text(
                              movie['title']?.toString() ?? 'Untitled',
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              textAlign: TextAlign.center,
                            ),
                          ),
                          IconButton(
                            tooltip: savedMovieIds.contains(id)
                                ? 'Remove from saved'
                                : 'Save movie',
                            onPressed: () => toggleSavedMovie(id),
                            icon: Icon(
                              savedMovieIds.contains(id)
                                  ? Icons.bookmark
                                  : Icons.bookmark_border,
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}
