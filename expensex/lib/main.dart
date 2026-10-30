import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
void main()=>runApp(const ExpenseX());
class ExpenseX extends StatelessWidget{const ExpenseX({super.key});@override Widget build(BuildContext c)=>MaterialApp(title:'ExpenseX',theme:ThemeData(colorSchemeSeed:Colors.teal,useMaterial3:true),home:const Home());}
class Entry{Entry(this.title,this.amount,this.date);final String title;final double amount;final DateTime date;Map<String,dynamic> json()=>{'title':title,'amount':amount,'date':date.toIso8601String()};factory Entry.from(Map<String,dynamic> j)=>Entry(j['title'],(j['amount'] as num).toDouble(),DateTime.parse(j['date']));}
class Home extends StatefulWidget{const Home({super.key});@override State<Home> createState()=>_HomeState();}
class _HomeState extends State<Home>{final title=TextEditingController(),amount=TextEditingController();List<Entry> entries=[];bool loading=true;
@override void initState(){super.initState();load();}
Future<void> load()async{final p=await SharedPreferences.getInstance();try{entries=(jsonDecode(p.getString('entries')??'[]') as List).map((x)=>Entry.from(Map<String,dynamic>.from(x))).toList();}catch(_){entries=[];}if(mounted)setState(()=>loading=false);}
Future<void> save()async{final p=await SharedPreferences.getInstance();await p.setString('entries',jsonEncode(entries.map((e)=>e.json()).toList()));}
double get total=>entries.fold(0,(s,e)=>s+e.amount);
Future<void> add()async{final t=title.text.trim(),a=double.tryParse(amount.text.trim());if(t.isEmpty||a==null||a<=0){ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Enter a title and positive amount')));return;}setState(()=>entries.insert(0,Entry(t,a,DateTime.now())));title.clear();amount.clear();await save();}
Future<void> remove(int i)async{setState(()=>entries.removeAt(i));await save();}
@override void dispose(){title.dispose();amount.dispose();super.dispose();}
@override Widget build(BuildContext c)=>Scaffold(appBar:AppBar(title:const Text('💸 ExpenseX')),body:loading?const Center(child:CircularProgressIndicator()):Padding(padding:const EdgeInsets.all(16),child:Column(children:[Card(child:ListTile(title:const Text('Total expenses'),subtitle:Text('\$'+total.toStringAsFixed(2),style:Theme.of(c).textTheme.headlineMedium),trailing:Text(entries.length.toString()+' records'))),TextField(controller:title,decoration:const InputDecoration(labelText:'Expense name')),TextField(controller:amount,keyboardType:const TextInputType.numberWithOptions(decimal:true),decoration:const InputDecoration(labelText:'Amount')),FilledButton(onPressed:add,child:const Text('Add expense')),Expanded(child:entries.isEmpty?const Center(child:Text('No expenses yet')):ListView.builder(itemCount:entries.length,itemBuilder:(c,i)=>Card(child:ListTile(title:Text(entries[i].title),subtitle:Text(entries[i].date.toLocal().toString()),trailing:Row(mainAxisSize:MainAxisSize.min,children:[Text('\$'+entries[i].amount.toStringAsFixed(2)),IconButton(onPressed:()=>remove(i),icon:const Icon(Icons.delete_outline))])))))])));}
