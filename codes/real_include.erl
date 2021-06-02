%% 简化erlang的include,减少内存使用

%%具体方案
%% 1. 通过词法分析找出每个erl,hrl代码中的包含的宏，record，使用的内部函数，定义的函数.
%% 2. 通过某个erl文件现用的include查找所有已经被include了的文件，在这些hrl文件中生成真正被需要的hrl.
%% 3. 手动删除include套include的代码
%% 4. 编译通过

-module(inc).
-author("yimo").
%% API
-compile(export_all).

add_system_lib_version({Any, Include}) ->
    [Dir | Rest] = filename:split(Include),
    Map = #{
        "cosTransactions" => "cosTransactions-1.3.3",
        "wx" => "wx-1.8.3",
        "cosEventDomain" => "cosEventDomain-1.2.2",
        "ssh" => "ssh-4.6.6",
        "et" => "et-1.6.1",
        "runtime_tools" => "runtime_tools-1.12.5",
        "cosNotification" => "cosNotification-1.2.3",
        "otp_mibs" => "otp_mibs-1.1.2",
        "parsetools" => "parsetools-2.1.6",
        "sasl" => "sasl-3.1.1",
        "inets" => "inets-6.5",
        "eldap" => "eldap-1.2.3",
        "rabbitmq_server" => "rabbitmq_server-2.7.0+dirty",
        "diameter" => "diameter-2.1.4",
        "dialyzer" => "dialyzer-3.2.4",
        "tools" => "tools-2.11.2",
        "cosFileTransfer" => "cosFileTransfer-1.2.2",
        "asn1" => "asn1-5.0.5",
        "ssl" => "ssl-8.2.4",
        "cosEvent" => "cosEvent-2.2.2",
        "xmerl" => "xmerl-1.3.16",
        "erts" => "erts-9.3",
        "erl_docgen" => "erl_docgen-0.7.2",
        "observer" => "observer-2.7",
        "kernel" => "kernel-5.4.3",
        "mnesia" => "mnesia-4.15.3",
        "edoc" => "edoc-0.9.2",
        "common_test" => "common_test-1.15.4",
        "public_key" => "public_key-1.5.2",
        "syntax_tools" => "syntax_tools-2.1.4",
        "stdlib" => "stdlib-3.4.4",
        "eunit" => "eunit-2.3.5",
        "reltool" => "reltool-0.7.5",
        "erl_interface" => "erl_interface-3.10.1",
        "hipe" => "hipe-3.17.1",
        "orber" => "orber-3.8.4",
        "snmp" => "snmp-5.2.10",
        "os_mon" => "os_mon-2.4.4",
        "compiler" => "compiler-7.1.5",
        "megaco" => "megaco-3.18.3",
        "cosProperty" => "cosProperty-1.2.3",
        "crypto" => "crypto-4.2.1",
        "debugger" => "debugger-4.2.4",
        "cosTime" => "cosTime-1.2.3",
        "ic" => "ic-4.4.3"
    },
    case Map of
        #{Dir := Version} ->
            {Any, filename:join([Version | Rest])};
        _ ->
            {Any, filename:join([Dir | Rest])}
    end.


system_macro() ->
    ['MODULE', 'FILE', 'FUNCTION_NAME', 'FUNCTION_NAME', 'FUNCTION_ARITY', 'LINE', 'MACHINE', 'MODULE_STRING'].

to_token(File) ->
    {ok, Code} = file:read_file(File),
    {ok, Token, _} = erl_scan:string(binary_to_list(Code)),
    Token.

include(File) ->
    F = fun(Include, Acc) ->
        I = add_system_lib_version(Include),
        [include_absolute_path(File, I) | Acc] end,
    lists:foldr(F, [], p_include(to_token(File), [])).
p_include([{'-', _}, {atom, _, include}, {'(', _}, {string, _, Include} | Rest], Acc) ->
    p_include(Rest, [{local, Include} | Acc]);
p_include([{'-', _}, {atom, _, include_lib}, {'(', _}, {string, _, Include} | Rest], Acc) ->
    p_include(Rest, [{lib, Include} | Acc]);
p_include([_ | Rest], Acc) ->
    p_include(Rest, Acc);
p_include([], Acc) ->
    Acc.

new_macro(File) ->
    sets:to_list(p_new_macro(to_token(File), sets:new())).
p_new_macro([{'-', _}, {atom, _, define}, {'(', _}, {var, _, NewMacro} | Rest], Acc) ->
    p_new_macro(Rest, sets:add_element(NewMacro, Acc));
p_new_macro([{'-', _}, {atom, _, define}, {'(', _}, {atom, _, NewMacro} | Rest], Acc) ->
    p_new_macro(Rest, sets:add_element(NewMacro, Acc));
p_new_macro([_ | Rest], Acc) ->
    p_new_macro(Rest, Acc);
p_new_macro([], Acc) ->
    Acc.

new_record(File) ->
    sets:to_list(p_new_record(to_token(File), sets:new())).
p_new_record([{'-', _}, {atom, _, record}, {'(', _}, {atom, _, NewRecord} | Rest], Acc) ->
    p_new_record(Rest, sets:add_element(NewRecord, Acc));
p_new_record([_ | Rest], Acc) ->
    p_new_record(Rest, Acc);
p_new_record([], Acc) ->
    Acc.


new_function(File) ->
    sets:to_list(p_new_function(to_token(File), sets:new())).
p_new_function([{'dot', _}, {atom, _, Function} | Rest], Acc) ->
    p_new_function(Rest, sets:add_element(Function, Acc));
p_new_function([_ | Rest], Acc) ->
    p_new_function(Rest, Acc);
p_new_function([], Acc) ->
    Acc.


require_macro(File) ->
    sets:to_list(p_require_macro(to_token(File), sets:new())) -- (new_macro(File) ++ system_macro()).
p_require_macro([{'?', _}, {var, _, Macro} | Rest], Acc) ->
    p_require_macro(Rest, sets:add_element(Macro, Acc));
p_require_macro([{'?', _}, {atom, _, Macro} | Rest], Acc) ->
    p_require_macro(Rest, sets:add_element(Macro, Acc));
p_require_macro([_ | Rest], Acc) ->
    p_require_macro(Rest, Acc);
p_require_macro([], Acc) ->
    Acc.

require_record(File) ->
    sets:to_list(p_require_record(to_token(File), sets:new())) -- new_record(File).
p_require_record([{'#', _}, {atom, _, Record} | Rest], Acc) ->
    p_require_record(Rest, sets:add_element(Record, Acc));
p_require_record([_ | Rest], Acc) ->
    p_require_record(Rest, Acc);
p_require_record([], Acc) ->
    Acc.


%% TODO: 原则上不通过include引入函数，暂时不做
require_function(File) ->
    sets:to_list(p_require_function(to_token(File), sets:new())) -- new_function(File).
p_require_function([{'atom', _}, {':', _}, {atom, _, _} | Rest], Acc) ->
    p_require_function(Rest, Acc);
p_require_function([{'atom', Function}, {'(', _} | Rest], Acc) ->
    p_require_function(Rest, sets:add_element(Function, Acc));
p_require_function([_ | Rest], Acc) ->
    p_require_function(Rest, Acc);
p_require_function([], Acc) ->
    Acc.


erl(Paths) ->
    F = fun(File, Acc) -> [File | Acc] end,
    lists:foldl(fun(Path, Acc) -> filelib:fold_files(Path, ".erl", true, F, []) ++ Acc end, [], Paths).

inverted_index(Key, Values) ->
    lists:foldl(fun(V, Acc) -> Acc#{V => Key} end, #{}, Values).

check_dup(M1, M2) ->
    F = fun(K, V1, _) ->
        maps:is_key(K, M1) andalso V1 =/= maps:get(K, M1) andalso
            not lists:member(K, ['IF'])

            andalso io:format("Same:~p ~n", [{K, V1, maps:get(K, M1)}]) end,
    maps:fold(F, '_', M2).

hrl_inverted_index(Hrls) ->
    F1 = fun(Hrl, {I1, I2}) ->
        NewMacro = new_macro(Hrl),
        NewRecord = new_record(Hrl),
        Im = inverted_index(Hrl, NewMacro),
        IR = inverted_index(Hrl, NewRecord),
        check_dup(I1, Im),
        check_dup(I2, IR),
        {maps:merge(I1, Im), maps:merge(I2, IR)}
         end,
    lists:foldl(F1, {#{}, #{}}, Hrls).


include_absolute_path(File, {local, Include}) ->
    false = filename:dirname(File) =:= File,
    I1 = filename:join([File, Include]),
    I2 = filename:join([File, "include", Include]), %% maybe not include?
    case {filelib:is_file(I1), filelib:is_file(I2)} of
        {true, false} -> I1;
        {false, true} -> I2;
        _ -> include_absolute_path(filename:dirname(File), {local, Include})
    end;

include_absolute_path(_, {lib, Include}) ->
    %% TODO: fix hard code
    Workdir = "/Users/yimo/workdir/deps",
    ERL_LIBS = "/usr/local/lib/erlang/lib",
    I1 = filename:join([Workdir, Include]),
    I2 = filename:join([ERL_LIBS, Include]),
    case {filelib:is_file(I1), filelib:is_file(I2)} of
        {true, false} -> I1;
        {false, true} -> I2;
        _ -> io:format("Can not find:~p", [Include]), throw(error)
    end.

dfs_include(File) ->
    Includes = include(File),
    lists:foldl(fun(Include, Acc) -> dfs_include(Include) ++ Acc end, [], Includes) ++ Includes.


endswith(Binary, Tail) ->
    size(Tail) =:= binary:longest_common_suffix([Binary, Tail]).


real_include(Erl) ->
    Hrls = dfs_include(Erl),
    {Im, IR} = hrl_inverted_index(Hrls),
    %% TODO: use dynamic programming
    F1 = fun(Require, Acc) ->
        Hrl = maps:get(Require, Im, null),
        Hrl =:= null andalso io:format("Require:~p~n", [{Erl, Require}]),
        sets:add_element(Hrl, Acc) end,
    F2 = fun(Require, Acc) ->
        Hrl = maps:get(Require, IR, null),
        Hrl =:= null andalso io:format("Require:~p~n", [{Erl, Require}]),
        sets:add_element(Hrl, Acc) end,
    sets:to_list(lists:foldl(F1, sets:new(), require_macro(Erl))) ++
    sets:to_list(lists:foldl(F2, sets:new(), require_record(Erl))).

main() ->
    Erls = erl(["/Users/yimo/workdir/abc/src"]),
    F = fun(Erl, Acc) -> Acc#{Erl => real_include(Erl)} end,
    Data = lists:foldl(F, #{}, Erls),
    M = maps:fold(fun(K, V, Acc) -> Acc#{list_to_binary(K) => lists:map(fun list_to_binary/1, V)} end, #{}, Data),
    file:write_file(<<"tmp.json">>, jiffy:encode(M)).


